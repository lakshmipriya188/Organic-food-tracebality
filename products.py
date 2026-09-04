"""Organic Foods product & category data model integrated with MySQL Category and Product tables."""

import os
from dataclasses import dataclass, field
from typing import List, Optional
import db_manager


@dataclass
class Category:
    category_id: int
    name: str
    slug: str
    description: str
    image_url: str
    item_count: int = 1


@dataclass
class Product:
    id: str
    category_id: int
    name: str
    slug: str
    category_slug: str
    price: float
    unit: str = "kg"
    original_price: Optional[float] = None
    coop_price: float = 0.0
    discount_pct: Optional[int] = None
    image_url: str = ""
    variants: List[str] = field(default_factory=lambda: ["500g", "1kg"])
    tags: List[str] = field(default_factory=list)
    rating: float = 4.9
    reviews_count: int = 142
    origin: str = "Organic Foods Farmer Cooperative"
    lab_cert: str = "NABL Accredited - 100% Pesticide Free"
    description: str = ""
    batch_no: str = "OF-BATCH-101"
    farmer_name: str = "Ramakrishnappa"
    farm_location: str = "Mandya Organic Belt, Karnataka"
    harvest_date: str = "2026-07-15"
    lab_test_cert: str = "NABL Accredited - Pass (0.00 ppm)"
    manufacture_date: str = "2026-07-20"
    expiry_date: str = "2027-07-20"
    quantity: int = 50
    onboarding_date: str = "2026-07-01"
    manufacturer_name: str = "Organic Produce Co-Op"

    @property
    def image_path(self) -> str:
        return self.image_url


def get_default_unit_for_category(category_id: int, product_name: str = "") -> str:
    """Return unit measure ('kg', 'g', or 'L') for products based on category and physical state.
    - Category 1 (Fruits), Category 2 (Vegetables), Category 3 (Grains), Category 4 (Pulses) & Category 6 (Spices): strictly kg
    - Category 5 (Dairy) & Category 7 (Beverages): strictly L (Litres)
    - Solid items: kg or g
    - Liquid items: L (Litre)
    """
    if category_id in (1, 2, 3, 4, 6):
        return "kg"
    if category_id in (5, 7):
        return "L"

    p_lower = product_name.lower()
    
    # Liquid items (Oils, Milk, Ghee, Juices, Beverages, Coconut Water, Sugarcane Juice, Buttermilk, Flavoured Milk, Almond Milk)
    liquid_keywords = [
        "oil", "milk", "juice", "beverage", "water", "ghee", "buttermilk", "drink"
    ]
    if category_id in (7, 10) or any(k in p_lower for k in liquid_keywords):
        if "tea" in p_lower or "coffee" in p_lower:
            return "g"  # Tea/coffee leaves or powder are solid
        return "L"
    
    # Solid items (g or kg)
    if category_id in (8) or any(k in p_lower for k in ["powder", "spice", "cardamom", "clove", "cinnamon", "butter", "cheese", "yogurt", "cream"]):
        return "g"
        
    return "kg"


def get_variants_for_unit(unit: str, category_id: int = 1, product_name: str = "") -> List[str]:
    """Return standard measures formatted for liquid (L/mL) vs solid (g/kg).
    For Category 1 (Fruits), Category 2 (Vegetables), Category 3 (Grains), Category 4 (Pulses) & Category 6 (Spices), variants are strictly in kg.
    For Category 5 (Dairy) & Category 7 (Beverages), variants are strictly in litres (1L, 2L, 5L).
    """
    if category_id in (1, 2, 3, 4, 6):
        return ["1kg", "2kg", "5kg"]
    if category_id in (5, 7):
        return ["1L", "2L", "5L"]

    p_lower = product_name.lower()
    u = unit.lower().strip()
    
    is_liquid = u in ("l", "litre", "1l", "ml") or category_id in (7, 10) or any(k in p_lower for k in ["oil", "milk", "juice", "water", "ghee", "buttermilk", "beverage"])
    if is_liquid and not ("tea" in p_lower or "coffee" in p_lower):
        return ["250mL", "500mL", "1L"]
    elif u == "kg":
        return ["1kg", "2kg", "5kg"]
    else:
        return ["250g", "500g", "1kg"]


def find_product_icon(product_name: str) -> str:
    """Find corresponding product image icon inside product_icons directory."""
    icon_dir = "product_icons"
    if not os.path.exists(icon_dir):
        return "assets/images/fruits.jpg"

    raw_name = product_name.strip()
    clean_name = (
        raw_name.replace("Organic ", "")
        .replace("Fresh ", "")
        .replace("Pure ", "")
        .replace("Ancient ", "")
        .replace("Cold Pressed ", "")
        .replace("Native ", "")
        .replace("Premium ", "")
        .strip()
    )

    files = os.listdir(icon_dir)
    candidates = [
        raw_name,
        clean_name,
        raw_name.replace("_", " "),
        clean_name.replace("_", " "),
        raw_name.replace(" ", "_"),
        clean_name.replace(" ", "_"),
    ]

    # 1. Exact match (case insensitive)
    for c in candidates:
        if not c:
            continue
        c_lower = c.lower().strip()
        for f in files:
            name_no_ext = os.path.splitext(f)[0].lower().strip()
            if c_lower == name_no_ext:
                return f"{icon_dir}/{f}"

    # 2. Substring match (case insensitive)
    for c in candidates:
        if not c or len(c.strip()) < 3:
            continue
        c_lower = c.lower().strip()
        for f in files:
            name_no_ext = os.path.splitext(f)[0].lower().strip()
            if c_lower in name_no_ext or name_no_ext in c_lower:
                return f"{icon_dir}/{f}"

    # 3. Individual word token matching
    words = [w.lower() for w in clean_name.split() if len(w) > 2]
    for w in words:
        for f in files:
            name_no_ext = os.path.splitext(f)[0].lower().strip()
            if w in name_no_ext:
                return f"{icon_dir}/{f}"

    return "assets/images/fruits.jpg"


# Default static fallback categories matching user SQL schema
FALLBACK_CATEGORIES = [
    Category(1, "Fruits", "fruits", "100% Organic Farm-Fresh Fruits", "assets/images/fruits.jpg"),
    Category(2, "Vegetables", "vegetables", "Fresh Organic Farm Vegetables", "assets/images/vegetables.jpg"),
    Category(3, "Grains", "grains", "Unpolished Traditional Whole Grains", "assets/images/grains.jpg"),
    Category(4, "Pulses", "pulses", "Sun-dried Native Organic Pulses", "assets/images/pulses.jpg"),
    Category(5, "Dairy", "dairy", "Pure A2 Desi Cow Dairy Products", "assets/images/dairy.jpg"),
    Category(6, "Spices", "spices", "Organic Aromatic Whole Spices", "assets/images/spices.jpg"),
    Category(7, "Beverages", "beverages", "Natural Organic Drinks & Juices", "assets/images/beverages.jpg"),
    Category(8, "Dry Fruits", "dry-fruits", "Premium Raw Organic Dry Fruits", "assets/images/dryfruit.jpg"),
    Category(9, "Millets", "millets", "Nutrient-rich Ancient Organic Millets", "assets/images/millets.jpg"),
    Category(10, "Oils", "oils", "Traditional Wooden Cold-Pressed Oils", "assets/images/oils.jpg"),
]

# Default static fallback products with category-specific units and measures (1kg/2kg/5kg for Cat 1-4 & 6, 1L/2L/5L for Cat 5 & 7)
FALLBACK_PRODUCTS = [
    # Category 1: 10 Fruits (units in kg, variants in kg only)
    Product(
        id="1", category_id=1, name="Organic Royal Gala Apple", slug="apple", category_slug="fruits",
        price=180.00, unit="kg", original_price=200.00, coop_price=162.00, discount_pct=10,
        image_url=find_product_icon("Apple"), quantity=50, manufacture_date="2026-07-20",
        expiry_date="2026-08-05", onboarding_date="2026-07-01", manufacturer_name="Mandya Organic Orchards",
        description="Farm-fresh handpicked crisp organic apples grown without synthetic pesticides.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="2", category_id=1, name="Organic Robusta Banana", slug="banana", category_slug="fruits",
        price=60.00, unit="kg", original_price=65.00, coop_price=54.00, discount_pct=8,
        image_url=find_product_icon("Banana"), quantity=80, manufacture_date="2026-07-22",
        expiry_date="2026-07-30", onboarding_date="2026-07-01", manufacturer_name="Maddur Riverbank Orchards",
        description="Naturally ripened chemical-free organic bananas packed with natural potassium.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="3", category_id=1, name="Organic Alphonso Mango", slug="mango", category_slug="fruits",
        price=350.00, unit="kg", original_price=400.00, coop_price=315.00, discount_pct=12,
        image_url=find_product_icon("Mango"), quantity=40, manufacture_date="2026-07-15",
        expiry_date="2026-07-28", onboarding_date="2026-07-01", manufacturer_name="Ratnagiri Heritage Mango Groves",
        description="Juicy and aromatic organic GI-tagged Alphonso mangoes.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="4", category_id=1, name="Organic Nagpur Orange", slug="orange", category_slug="fruits",
        price=90.00, unit="kg", original_price=100.00, coop_price=81.00, discount_pct=10,
        image_url=find_product_icon("Orange"), quantity=60, manufacture_date="2026-07-18",
        expiry_date="2026-08-08", onboarding_date="2026-07-01", manufacturer_name="Nagpur Citrus Growers Co-op",
        description="Sweet and vitamin C rich farm-fresh organic oranges.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="5", category_id=1, name="Organic Red Pomegranate", slug="pomegranate", category_slug="fruits",
        price=220.00, unit="kg", original_price=250.00, coop_price=198.00, discount_pct=12,
        image_url=find_product_icon("Pomegranate"), quantity=45, manufacture_date="2026-07-19",
        expiry_date="2026-08-15", onboarding_date="2026-07-01", manufacturer_name="Solapur Organic Farms",
        description="Ruby-red antioxidant-rich premium organic pomegranates.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="6", category_id=1, name="Organic Pink Guava", slug="guava", category_slug="fruits",
        price=80.00, unit="kg", original_price=85.00, coop_price=72.00, discount_pct=6,
        image_url=find_product_icon("Guava"), quantity=55, manufacture_date="2026-07-21",
        expiry_date="2026-08-01", onboarding_date="2026-07-01", manufacturer_name="Kolar Fruit Growers",
        description="Crunchy and sweet pink-fleshed organic guavas.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="7", category_id=1, name="Organic Hybrid Watermelon", slug="watermelon", category_slug="fruits",
        price=40.00, unit="kg", original_price=45.00, coop_price=36.00, discount_pct=10,
        image_url=find_product_icon("Watermelon"), quantity=70, manufacture_date="2026-07-24",
        expiry_date="2026-08-10", onboarding_date="2026-07-01", manufacturer_name="Challakere Riverbed Farms",
        description="Hydrating and naturally sweet organic watermelons.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="8", category_id=1, name="Organic Pink Dragon Fruit", slug="dragon-fruit", category_slug="fruits",
        price=250.00, unit="kg", original_price=290.00, coop_price=225.00, discount_pct=14,
        image_url=find_product_icon("Dragon Fruit"), quantity=30, manufacture_date="2026-07-23",
        expiry_date="2026-08-07", onboarding_date="2026-07-01", manufacturer_name="Deccan Exotic Fruit Farms",
        description="Exotic nutrient-dense organic pink dragon fruit.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="9", category_id=1, name="Organic Queen Pineapple", slug="pineapple", category_slug="fruits",
        price=110.00, unit="kg", original_price=120.00, coop_price=99.00, discount_pct=8,
        image_url=find_product_icon("Pineapple"), quantity=40, manufacture_date="2026-07-17",
        expiry_date="2026-08-07", onboarding_date="2026-07-01", manufacturer_name="Shivamogga Foothill Orchards",
        description="Tropical aromatic sweet organic queen pineapples.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="10", category_id=1, name="Organic Sweet Lime (Mosambi)", slug="sweet-lime", category_slug="fruits",
        price=95.00, unit="kg", original_price=105.00, coop_price=85.50, discount_pct=9,
        image_url=find_product_icon("Sweet Lime"), quantity=50, manufacture_date="2026-07-20",
        expiry_date="2026-08-10", onboarding_date="2026-07-01", manufacturer_name="Anantapur Fruit Orchards",
        description="Fresh juicy organic sweet lime full of natural electrolytes.",
        variants=["1kg", "2kg", "5kg"]
    ),
    # Category 2: 10 Vegetables (units in kg, variants in kg only)
    Product(
        id="11", category_id=2, name="Organic Country Tomato", slug="tomato", category_slug="vegetables",
        price=45.00, unit="kg", original_price=50.00, coop_price=40.50, discount_pct=10,
        image_url=find_product_icon("Tomato"), quantity=100, manufacture_date="2026-07-25",
        expiry_date="2026-08-05", onboarding_date="2026-07-01", manufacturer_name="Maddur Riverbank Farms",
        description="Naturally grown fresh organic country tomatoes.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="12", category_id=2, name="Organic Fresh Potato", slug="potato", category_slug="vegetables",
        price=35.00, unit="kg", original_price=40.00, coop_price=31.50, discount_pct=12,
        image_url=find_product_icon("Potato"), quantity=120, manufacture_date="2026-07-20",
        expiry_date="2026-08-20", onboarding_date="2026-07-01", manufacturer_name="Hassan Organic Potato Growers",
        description="Earth-fresh farm-grown organic potatoes rich in natural energy.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="13", category_id=2, name="Organic Red Onion", slug="onion", category_slug="vegetables",
        price=40.00, unit="kg", original_price=45.00, coop_price=36.00, discount_pct=11,
        image_url=find_product_icon("Onion"), quantity=150, manufacture_date="2026-07-18",
        expiry_date="2026-08-30", onboarding_date="2026-07-01", manufacturer_name="Chitradurga Farm Collective",
        description="Crisp and pungent sun-dried organic red onions.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="14", category_id=2, name="Organic Farm Carrot", slug="carrot", category_slug="vegetables",
        price=60.00, unit="kg", original_price=70.00, coop_price=54.00, discount_pct=14,
        image_url=find_product_icon("Carrot"), quantity=90, manufacture_date="2026-07-24",
        expiry_date="2026-08-10", onboarding_date="2026-07-01", manufacturer_name="Ooty Hill Organic Orchards",
        description="Sweet crunchy beta-carotene rich organic carrots.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="15", category_id=2, name="Organic Green Cabbage", slug="cabbage", category_slug="vegetables",
        price=30.00, unit="kg", original_price=35.00, coop_price=27.00, discount_pct=14,
        image_url=find_product_icon("Cabbage"), quantity=80, manufacture_date="2026-07-26",
        expiry_date="2026-08-08", onboarding_date="2026-07-01", manufacturer_name="Kolar Veg Growers",
        description="Fresh compact pesticide-free organic green cabbage.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="16", category_id=2, name="Organic Fresh Cauliflower", slug="cauliflower", category_slug="vegetables",
        price=50.00, unit="kg", original_price=55.00, coop_price=45.00, discount_pct=9,
        image_url=find_product_icon("Cauliflower"), quantity=70, manufacture_date="2026-07-25",
        expiry_date="2026-08-03", onboarding_date="2026-07-01", manufacturer_name="Belagavi Farm Co-Op",
        description="Tender white florets of naturally grown organic cauliflower.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="17", category_id=2, name="Organic Green Capsicum", slug="capsicum", category_slug="vegetables",
        price=80.00, unit="kg", original_price=90.00, coop_price=72.00, discount_pct=11,
        image_url=find_product_icon("Capsicum"), quantity=65, manufacture_date="2026-07-23",
        expiry_date="2026-08-04", onboarding_date="2026-07-01", manufacturer_name="Mandya Polyhouse Organic Farms",
        description="Crisp glossy antioxidant-rich organic bell peppers.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="18", category_id=2, name="Organic Purple Brinjal", slug="brinjal", category_slug="vegetables",
        price=40.00, unit="kg", original_price=45.00, coop_price=36.00, discount_pct=11,
        image_url=find_product_icon("Brinjal"), quantity=75, manufacture_date="2026-07-22",
        expiry_date="2026-08-02", onboarding_date="2026-07-01", manufacturer_name="Tumakuru Farm Collective",
        description="Tender and glossy native organic purple eggplants.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="19", category_id=2, name="Organic Ruby Beetroot", slug="beetroot", category_slug="vegetables",
        price=50.00, unit="kg", original_price=55.00, coop_price=45.00, discount_pct=9,
        image_url=find_product_icon("Beetroot"), quantity=85, manufacture_date="2026-07-21",
        expiry_date="2026-08-15", onboarding_date="2026-07-01", manufacturer_name="Chikkaballapur Organic Belt",
        description="Nutrient-dense sweet organic ruby red beetroots.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="20", category_id=2, name="Organic Sweet Corn", slug="corn", category_slug="vegetables",
        price=45.00, unit="kg", original_price=50.00, coop_price=40.50, discount_pct=10,
        image_url=find_product_icon("Corn"), quantity=110, manufacture_date="2026-07-24",
        expiry_date="2026-08-06", onboarding_date="2026-07-01", manufacturer_name="Davanagere Grain & Produce Co-op",
        description="Juicy golden kernels of farm-fresh organic sweet corn.",
        variants=["1kg", "2kg", "5kg"]
    ),
    # Category 3: 10 Grains (units in kg, variants in kg only)
    Product(
        id="21", category_id=3, name="Organic Unpolished Brown Rice", slug="brown-rice", category_slug="grains",
        price=150.00, unit="kg", original_price=175.00, coop_price=135.00, discount_pct=14,
        image_url=find_product_icon("Brown Rice"), quantity=200, manufacture_date="2026-07-10",
        expiry_date="2027-07-10", onboarding_date="2026-07-01", manufacturer_name="Mysuru Heritage Paddy Farms",
        description="Unpolished traditional brown rice rich in natural bran fiber.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="22", category_id=3, name="Organic Khapli Whole Wheat", slug="wheat", category_slug="grains",
        price=85.00, unit="kg", original_price=95.00, coop_price=76.50, discount_pct=10,
        image_url=find_product_icon("Wheat"), quantity=250, manufacture_date="2026-07-12",
        expiry_date="2027-07-12", onboarding_date="2026-07-01", manufacturer_name="Bagalkot Native Farmers Co-Op",
        description="Ancient low-GI emmer whole wheat grains.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="23", category_id=3, name="Organic Pearl Barley Grain", slug="barley", category_slug="grains",
        price=110.00, unit="kg", original_price=125.00, coop_price=99.00, discount_pct=12,
        image_url=find_product_icon("Barley"), quantity=140, manufacture_date="2026-07-14",
        expiry_date="2027-07-14", onboarding_date="2026-07-01", manufacturer_name="Himalayan Valley Organics",
        description="Nutrient-dense cooling pearl barley grains.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="24", category_id=3, name="Organic Raw Buckwheat (Kuttu)", slug="buckwheat", category_slug="grains",
        price=160.00, unit="kg", original_price=180.00, coop_price=144.00, discount_pct=11,
        image_url=find_product_icon("Buckwheat"), quantity=110, manufacture_date="2026-07-16",
        expiry_date="2027-07-16", onboarding_date="2026-07-01", manufacturer_name="Uttarakhand Mountain Produce",
        description="Gluten-free nutrient-rich raw buckwheat grains.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="25", category_id=3, name="Organic White Quinoa Grain", slug="quinoa", category_slug="grains",
        price=280.00, unit="kg", original_price=320.00, coop_price=252.00, discount_pct=12,
        image_url=find_product_icon("Quinoa"), quantity=90, manufacture_date="2026-07-18",
        expiry_date="2027-07-18", onboarding_date="2026-07-01", manufacturer_name="Deccan Plateau Quinoa Project",
        description="Complete protein-rich royal white quinoa seeds.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="26", category_id=3, name="Organic Whole Rolled Oats", slug="oats", category_slug="grains",
        price=190.00, unit="kg", original_price=210.00, coop_price=171.00, discount_pct=9,
        image_url=find_product_icon("Oats"), quantity=130, manufacture_date="2026-07-20",
        expiry_date="2027-07-20", onboarding_date="2026-07-01", manufacturer_name="Nilgiri Organic Grain Mill",
        description="Heart-healthy fiber rich organic rolled oats.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="27", category_id=3, name="Organic Whole Rye Grain", slug="rye", category_slug="grains",
        price=140.00, unit="kg", original_price=155.00, coop_price=126.00, discount_pct=10,
        image_url=find_product_icon("Rye"), quantity=100, manufacture_date="2026-07-22",
        expiry_date="2027-07-22", onboarding_date="2026-07-01", manufacturer_name="Coorg Organic Grain Guild",
        description="Traditional wholesome organic rye grains.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="28", category_id=3, name="Organic Jowar Whole Grain", slug="sorghum", category_slug="grains",
        price=95.00, unit="kg", original_price=105.00, coop_price=85.50, discount_pct=9,
        image_url=find_product_icon("Sorghum"), quantity=180, manufacture_date="2026-07-15",
        expiry_date="2027-07-15", onboarding_date="2026-07-01", manufacturer_name="Raichur Dryland Grain Co-op",
        description="Gluten-free wholesome white jowar sorghum grains.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="29", category_id=3, name="Organic Traditional Basmati Rice", slug="basmati-rice", category_slug="grains",
        price=220.00, unit="kg", original_price=250.00, coop_price=198.00, discount_pct=12,
        image_url=find_product_icon("Brown Rice"), quantity=160, manufacture_date="2026-07-11",
        expiry_date="2027-07-11", onboarding_date="2026-07-01", manufacturer_name="Tarai Foothill Organic Farmers",
        description="Aromatic long-grain aged organic basmati rice.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="30", category_id=3, name="Organic Kerala Red Matta Rice", slug="matta-rice", category_slug="grains",
        price=130.00, unit="kg", original_price=145.00, coop_price=117.00, discount_pct=10,
        image_url=find_product_icon("Brown Rice"), quantity=150, manufacture_date="2026-07-13",
        expiry_date="2027-07-13", onboarding_date="2026-07-01", manufacturer_name="Palakkad Paddy Farmers Collective",
        description="Coarse nutrient-dense traditional red matta rice.",
        variants=["1kg", "2kg", "5kg"]
    ),
    # Category 4: 10 Pulses (units in kg, variants in kg only)
    Product(
        id="31", category_id=4, name="Organic Unpolished Toor Dal (Arhar)", slug="toor-dal", category_slug="pulses",
        price=180.00, unit="kg", original_price=200.00, coop_price=162.00, discount_pct=10,
        image_url=find_product_icon("Toor Dal"), quantity=150, manufacture_date="2026-07-12",
        expiry_date="2027-01-12", onboarding_date="2026-07-01", manufacturer_name="Kalaburagi Pulse Collective",
        description="Sun-dried protein-dense native organic toor dal.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="32", category_id=4, name="Organic Split Red Lentil (Masoor Dal)", slug="masoor-dal", category_slug="pulses",
        price=140.00, unit="kg", original_price=155.00, coop_price=126.00, discount_pct=10,
        image_url=find_product_icon("Masoor Dal"), quantity=160, manufacture_date="2026-07-14",
        expiry_date="2027-01-14", onboarding_date="2026-07-01", manufacturer_name="Indore Lentil Growers Co-op",
        description="Easy-to-cook protein-rich organic red split masoor dal.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="33", category_id=4, name="Organic Kabuli Chickpeas (Chana)", slug="chickpeas", category_slug="pulses",
        price=160.00, unit="kg", original_price=180.00, coop_price=144.00, discount_pct=11,
        image_url=find_product_icon("Chickpeas"), quantity=140, manufacture_date="2026-07-15",
        expiry_date="2027-01-15", onboarding_date="2026-07-01", manufacturer_name="Malwa Plateau Organic Farms",
        description="Large nutty organic kabuli chickpeas rich in fiber and protein.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="34", category_id=4, name="Organic Whole Black Gram (Urad Whole)", slug="black-gram", category_slug="pulses",
        price=175.00, unit="kg", original_price=195.00, coop_price=157.50, discount_pct=10,
        image_url=find_product_icon("Black Gram"), quantity=130, manufacture_date="2026-07-18",
        expiry_date="2027-01-18", onboarding_date="2026-07-01", manufacturer_name="Andhra Organic Pulse Growers",
        description="Traditional unpolished whole black urad dal.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="35", category_id=4, name="Organic Whole Green Moong Dal", slug="green-gram", category_slug="pulses",
        price=155.00, unit="kg", original_price=170.00, coop_price=139.50, discount_pct=9,
        image_url=find_product_icon("Green Gram"), quantity=170, manufacture_date="2026-07-16",
        expiry_date="2027-01-16", onboarding_date="2026-07-01", manufacturer_name="Rajasthan Rainfed Farmers Co-Op",
        description="Wholesome pesticide-free whole green moong dal.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="36", category_id=4, name="Organic Native Horse Gram (Kollu)", slug="horse-gram", category_slug="pulses",
        price=120.00, unit="kg", original_price=135.00, coop_price=108.00, discount_pct=11,
        image_url=find_product_icon("Horse Gram"), quantity=120, manufacture_date="2026-07-13",
        expiry_date="2027-01-13", onboarding_date="2026-07-01", manufacturer_name="Kongu Region Native Seed Growers",
        description="Iron and protein-rich traditional native horse gram.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="37", category_id=4, name="Organic Brown Cowpeas (Lobia)", slug="cowpeas", category_slug="pulses",
        price=130.00, unit="kg", original_price=145.00, coop_price=117.00, discount_pct=10,
        image_url=find_product_icon("Cowpeas"), quantity=110, manufacture_date="2026-07-17",
        expiry_date="2027-01-17", onboarding_date="2026-07-01", manufacturer_name="Deccan Grain Guild",
        description="Tender and nutty organic brown cowpeas.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="38", category_id=4, name="Organic Kashmiri Rajma (Kidney Beans)", slug="kidney-beans", category_slug="pulses",
        price=195.00, unit="kg", original_price=220.00, coop_price=175.50, discount_pct=11,
        image_url=find_product_icon("Kidney Beans"), quantity=100, manufacture_date="2026-07-19",
        expiry_date="2027-01-19", onboarding_date="2026-07-01", manufacturer_name="Bhaderwah Valley Organics",
        description="Authentic small dark red Kashmiri rajma kidney beans.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="39", category_id=4, name="Organic Dried White Peas (Safed Matar)", slug="white-peas", category_slug="pulses",
        price=110.00, unit="kg", original_price=125.00, coop_price=99.00, discount_pct=12,
        image_url=find_product_icon("White Peas"), quantity=125, manufacture_date="2026-07-21",
        expiry_date="2027-01-21", onboarding_date="2026-07-01", manufacturer_name="Bundelkhand Farmers Co-op",
        description="Clean sun-dried organic white peas rich in minerals.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="40", category_id=4, name="Organic Native Yellow Soybeans", slug="soybeans", category_slug="pulses",
        price=135.00, unit="kg", original_price=150.00, coop_price=121.50, discount_pct=10,
        image_url=find_product_icon("Soybeans"), quantity=135, manufacture_date="2026-07-20",
        expiry_date="2027-01-20", onboarding_date="2026-07-01", manufacturer_name="Latur Organic Soybean Cluster",
        description="Non-GMO protein-packed organic yellow soybeans.",
        variants=["1kg", "2kg", "5kg"]
    ),
    # Category 5: 10 Dairy Products (units in L, variants in L only)
    Product(
        id="41", category_id=5, name="Organic Pure A2 Desi Cow Milk", slug="a2-milk", category_slug="dairy",
        price=95.00, unit="L", original_price=110.00, coop_price=85.50, discount_pct=14,
        image_url=find_product_icon("Milk"), quantity=100, manufacture_date="2026-07-28",
        expiry_date="2026-07-31", onboarding_date="2026-07-01", manufacturer_name="Pandavapura Bilona Dairy",
        description="Pure unpasteurized fresh A2 Desi Cow milk.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="42", category_id=5, name="Organic Farm Fresh Buffalo Milk", slug="buffalo-milk", category_slug="dairy",
        price=85.00, unit="L", original_price=95.00, coop_price=76.50, discount_pct=10,
        image_url=find_product_icon("Milk"), quantity=120, manufacture_date="2026-07-28",
        expiry_date="2026-07-31", onboarding_date="2026-07-01", manufacturer_name="Davanagere Dairy Co-Op",
        description="Rich and creamy fresh organic buffalo milk.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="43", category_id=5, name="Organic Badam Flavoured Milk", slug="badam-milk", category_slug="dairy",
        price=140.00, unit="L", original_price=160.00, coop_price=126.00, discount_pct=12,
        image_url=find_product_icon("Flavoured Milk"), quantity=80, manufacture_date="2026-07-26",
        expiry_date="2026-08-05", onboarding_date="2026-07-01", manufacturer_name="Heritage Organic Dairies",
        description="Nourishing A2 milk infused with real organic almonds.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="44", category_id=5, name="Organic Traditional Spiced Buttermilk (Chaas)", slug="buttermilk", category_slug="dairy",
        price=60.00, unit="L", original_price=70.00, coop_price=54.00, discount_pct=14,
        image_url=find_product_icon("Buttermilk"), quantity=150, manufacture_date="2026-07-27",
        expiry_date="2026-08-02", onboarding_date="2026-07-01", manufacturer_name="Malnad Organic Dairy Guild",
        description="Refreshing churned buttermilk spiced with cumin and curry leaves.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="45", category_id=5, name="Organic A2 Desi Cow Bilona Ghee", slug="ghee", category_slug="dairy",
        price=1450.00, unit="L", original_price=1600.00, coop_price=1305.00, discount_pct=9,
        image_url=find_product_icon("Ghee"), quantity=60, manufacture_date="2026-07-15",
        expiry_date="2027-07-15", onboarding_date="2026-07-01", manufacturer_name="Gir Organic Cow Sanctuary",
        description="Traditional Vedic bilona method cultured A2 ghee.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="46", category_id=5, name="Organic Fresh Creamy Set Curd (Dahi)", slug="curd", category_slug="dairy",
        price=110.00, unit="L", original_price=125.00, coop_price=99.00, discount_pct=12,
        image_url=find_product_icon("Curd"), quantity=90, manufacture_date="2026-07-27",
        expiry_date="2026-08-03", onboarding_date="2026-07-01", manufacturer_name="Mandya Artisan Dairy",
        description="Thick naturally set probiotic curd made from A2 cow milk.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="47", category_id=5, name="Organic Raw Almond Milk", slug="almond-milk", category_slug="dairy",
        price=220.00, unit="L", original_price=250.00, coop_price=198.00, discount_pct=12,
        image_url=find_product_icon("Almond Milk"), quantity=70, manufacture_date="2026-07-26",
        expiry_date="2026-08-04", onboarding_date="2026-07-01", manufacturer_name="Plant-Based Organic Dairies",
        description="Lactose-free creamy cold-pressed raw almond milk.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="48", category_id=5, name="Organic Fresh Farm Malai Cream", slug="cream", category_slug="dairy",
        price=350.00, unit="L", original_price=390.00, coop_price=315.00, discount_pct=10,
        image_url=find_product_icon("Cream"), quantity=50, manufacture_date="2026-07-27",
        expiry_date="2026-08-02", onboarding_date="2026-07-01", manufacturer_name="Hassan Dairy Farmers Co-Op",
        description="Pure unadulterated thick fresh farm malai cream.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="49", category_id=5, name="Organic Kesar Pista Flavoured Milk", slug="kesar-milk", category_slug="dairy",
        price=160.00, unit="L", original_price=180.00, coop_price=144.00, discount_pct=11,
        image_url=find_product_icon("Flavoured Milk"), quantity=75, manufacture_date="2026-07-26",
        expiry_date="2026-08-05", onboarding_date="2026-07-01", manufacturer_name="Royal Organic Dairy Craft",
        description="A2 milk blended with organic saffron strands and pistachios.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="50", category_id=5, name="Organic Sweet Mango Lassi", slug="mango-lassi", category_slug="dairy",
        price=120.00, unit="L", original_price=135.00, coop_price=108.00, discount_pct=11,
        image_url=find_product_icon("Buttermilk"), quantity=85, manufacture_date="2026-07-27",
        expiry_date="2026-08-03", onboarding_date="2026-07-01", manufacturer_name="Ratnagiri Fruit Dairy Collective",
        description="Rich churned yogurt drink blended with Alphonso mango pulp.",
        variants=["1L", "2L", "5L"]
    ),
    # Category 6: 10 Spices (units in kg, variants in kg only)
    Product(
        id="51", category_id=6, name="Organic Salem Whole Turmeric & Powder", slug="turmeric", category_slug="spices",
        price=210.00, unit="kg", original_price=230.00, coop_price=189.00, discount_pct=8,
        image_url=find_product_icon("Turmeric Powder"), quantity=80, manufacture_date="2026-07-05",
        expiry_date="2027-07-05", onboarding_date="2026-07-01", manufacturer_name="Sirsi Spice Hills Garden",
        description="Aromatic high-curcumin Salem organic turmeric.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="52", category_id=6, name="Organic Guntur Red Chilli Powder", slug="chilli-powder", category_slug="spices",
        price=280.00, unit="kg", original_price=310.00, coop_price=252.00, discount_pct=10,
        image_url=find_product_icon("Chilli Powder"), quantity=100, manufacture_date="2026-07-08",
        expiry_date="2027-07-08", onboarding_date="2026-07-01", manufacturer_name="Guntur Chilli Spice Co-Op",
        description="Sun-dried fiery red Guntur chilli powder.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="53", category_id=6, name="Organic Native Coriander Seeds (Dhania)", slug="coriander", category_slug="spices",
        price=160.00, unit="kg", original_price=180.00, coop_price=144.00, discount_pct=11,
        image_url=find_product_icon("Coriander Powder"), quantity=120, manufacture_date="2026-07-10",
        expiry_date="2027-07-10", onboarding_date="2026-07-01", manufacturer_name="Ramganj Mandi Spice Guild",
        description="Fragrant whole native coriander seeds.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="54", category_id=6, name="Organic Whole Cumin Seeds (Jeera)", slug="cumin", category_slug="spices",
        price=320.00, unit="kg", original_price=360.00, coop_price=288.00, discount_pct=11,
        image_url=find_product_icon("Cumin Seeds"), quantity=90, manufacture_date="2026-07-12",
        expiry_date="2027-07-12", onboarding_date="2026-07-01", manufacturer_name="Unjha Organic Cumin Collective",
        description="Aromatic sun-cured whole cumin seeds.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="55", category_id=6, name="Organic Malabar Black Pepper", slug="black-pepper", category_slug="spices",
        price=650.00, unit="kg", original_price=720.00, coop_price=585.00, discount_pct=10,
        image_url=find_product_icon("Black Pepper"), quantity=70, manufacture_date="2026-07-14",
        expiry_date="2027-07-14", onboarding_date="2026-07-01", manufacturer_name="Wayanad Spice Plantation",
        description="Bold aromatic GI-tagged Malabar black peppercorns.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="56", category_id=6, name="Organic Green Cardamom (Elaichi)", slug="cardamom", category_slug="spices",
        price=2200.00, unit="kg", original_price=2500.00, coop_price=1980.00, discount_pct=12,
        image_url=find_product_icon("Cardamom"), quantity=40, manufacture_date="2026-07-15",
        expiry_date="2027-07-15", onboarding_date="2026-07-01", manufacturer_name="Idukki Cardamom Hills Co-Op",
        description="Plump fragrant 8mm green cardamom pods.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="57", category_id=6, name="Organic Ceylon Cinnamon Sticks", slug="cinnamon", category_slug="spices",
        price=950.00, unit="kg", original_price=1050.00, coop_price=855.00, discount_pct=9,
        image_url=find_product_icon("Cinnamon"), quantity=60, manufacture_date="2026-07-16",
        expiry_date="2027-07-16", onboarding_date="2026-07-01", manufacturer_name="Southern Spice Estate",
        description="Sweet delicate true Ceylon cinnamon quills.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="58", category_id=6, name="Organic Malnad Whole Cloves (Laung)", slug="cloves", category_slug="spices",
        price=1100.00, unit="kg", original_price=1250.00, coop_price=990.00, discount_pct=12,
        image_url=find_product_icon("Cloves"), quantity=50, manufacture_date="2026-07-17",
        expiry_date="2027-07-17", onboarding_date="2026-07-01", manufacturer_name="Shimoga Organic Spice Belt",
        description="Aroma-rich whole handpicked cloves.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="59", category_id=6, name="Organic Sweet Fennel Seeds (Saunf)", slug="fennel", category_slug="spices",
        price=190.00, unit="kg", original_price=210.00, coop_price=171.00, discount_pct=9,
        image_url=find_product_icon("Fennel Seeds"), quantity=110, manufacture_date="2026-07-18",
        expiry_date="2027-07-18", onboarding_date="2026-07-01", manufacturer_name="Saurashtra Spice Farmers",
        description="Sweet aromatic digestive green fennel seeds.",
        variants=["1kg", "2kg", "5kg"]
    ),
    Product(
        id="60", category_id=6, name="Organic Whole Fenugreek Seeds (Methi)", slug="fenugreek", category_slug="spices",
        price=140.00, unit="kg", original_price=155.00, coop_price=126.00, discount_pct=10,
        image_url=find_product_icon("Fenugreek"), quantity=130, manufacture_date="2026-07-19",
        expiry_date="2027-07-19", onboarding_date="2026-07-01", manufacturer_name="Nagaur Spice Collective",
        description="Golden bitter-sweet organic fenugreek seeds.",
        variants=["1kg", "2kg", "5kg"]
    ),
    # Category 7: 10 Beverages (units in L, variants in L only)
    Product(
        id="61", category_id=7, name="Organic Fresh Mixed Fruit Juice", slug="fruit-juice", category_slug="beverages",
        price=135.00, unit="L", original_price=150.00, coop_price=121.50, discount_pct=10,
        image_url=find_product_icon("Fruit Juice"), quantity=60, manufacture_date="2026-07-18",
        expiry_date="2026-10-18", onboarding_date="2026-07-01", manufacturer_name="Chikmagalur Herbal Valley",
        description="Revitalizing natural organic herbal fruit drink bottled fresh.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="62", category_id=7, name="Organic Tender Coconut Water", slug="coconut-water", category_slug="beverages",
        price=90.00, unit="L", original_price=100.00, coop_price=81.00, discount_pct=10,
        image_url=find_product_icon("Coconut Water"), quantity=120, manufacture_date="2026-07-28",
        expiry_date="2026-08-05", onboarding_date="2026-07-01", manufacturer_name="Pollachi Coconut Farmers Co-Op",
        description="Pure hydrating electrolyte-rich organic tender coconut water.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="63", category_id=7, name="Organic Raw Sugarcane Juice", slug="sugarcane-juice", category_slug="beverages",
        price=80.00, unit="L", original_price=90.00, coop_price=72.00, discount_pct=11,
        image_url=find_product_icon("Fruit Juice"), quantity=100, manufacture_date="2026-07-28",
        expiry_date="2026-08-02", onboarding_date="2026-07-01", manufacturer_name="Mandya Sugarcane Organic Belt",
        description="Cold-pressed raw organic sugarcane juice with ginger and lime.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="64", category_id=7, name="Organic Cold-Pressed Wild Amla Juice", slug="amla-juice", category_slug="beverages",
        price=160.00, unit="L", original_price=180.00, coop_price=144.00, discount_pct=11,
        image_url=find_product_icon("Fruit Juice"), quantity=80, manufacture_date="2026-07-20",
        expiry_date="2026-11-20", onboarding_date="2026-07-01", manufacturer_name="Pratapgarh Wild Amla Collective",
        description="Vitamin C packed pure cold-pressed wild amla juice.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="65", category_id=7, name="Organic Konkan Kokum Sherbet Concentrate", slug="kokum-sherbet", category_slug="beverages",
        price=175.00, unit="L", original_price=195.00, coop_price=157.50, discount_pct=10,
        image_url=find_product_icon("Fruit Juice"), quantity=70, manufacture_date="2026-07-15",
        expiry_date="2027-01-15", onboarding_date="2026-07-01", manufacturer_name="Ratnagiri Organic Produce Guild",
        description="Tangy digestive organic kokum fruit extract.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="66", category_id=7, name="Organic Fresh Mint Lemonade", slug="lemonade", category_slug="beverages",
        price=85.00, unit="L", original_price=95.00, coop_price=76.50, discount_pct=10,
        image_url=find_product_icon("Lemonade"), quantity=90, manufacture_date="2026-07-27",
        expiry_date="2026-08-05", onboarding_date="2026-07-01", manufacturer_name="Nilgiri Mint & Citrus Orchards",
        description="Zesty refreshing lemonade infused with farm-fresh mint.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="67", category_id=7, name="Organic Traditional Nannari Roots Sherbet", slug="nannari-sherbet", category_slug="beverages",
        price=150.00, unit="L", original_price=170.00, coop_price=135.00, discount_pct=12,
        image_url=find_product_icon("Fruit Juice"), quantity=75, manufacture_date="2026-07-10",
        expiry_date="2027-01-10", onboarding_date="2026-07-01", manufacturer_name="Western Ghats Herbal Collective",
        description="Cooling traditional Indian sarsaparilla root extract drink.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="68", category_id=7, name="Organic Pure Aloe Vera Drink", slug="aloe-vera-drink", category_slug="beverages",
        price=140.00, unit="L", original_price=160.00, coop_price=126.00, discount_pct=12,
        image_url=find_product_icon("Fruit Juice"), quantity=85, manufacture_date="2026-07-22",
        expiry_date="2026-11-22", onboarding_date="2026-07-01", manufacturer_name="Thar Desert Organic Aloe Farms",
        description="Hydrating aloe vera pulp juice with natural fiber.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="69", category_id=7, name="Organic Alphonso Mango Nectar Juice", slug="mango-nectar", category_slug="beverages",
        price=190.00, unit="L", original_price=215.00, coop_price=171.00, discount_pct=11,
        image_url=find_product_icon("Fruit Juice"), quantity=80, manufacture_date="2026-07-25",
        expiry_date="2026-10-25", onboarding_date="2026-07-01", manufacturer_name="Devgad Heritage Mango Groves",
        description="Thick luscious GI Alphonso mango pulp juice.",
        variants=["1L", "2L", "5L"]
    ),
    Product(
        id="70", category_id=7, name="Organic Fresh Red Pomegranate Juice", slug="pomegranate-juice", category_slug="beverages",
        price=210.00, unit="L", original_price=240.00, coop_price=189.00, discount_pct=12,
        image_url=find_product_icon("Fruit Juice"), quantity=65, manufacture_date="2026-07-26",
        expiry_date="2026-08-10", onboarding_date="2026-07-01", manufacturer_name="Solapur Pomegranate Juices",
        description="Pure 100% pressed red pomegranate juice no added sugar.",
        variants=["1L", "2L", "5L"]
    ),
    # Other Categories
    Product(
        id="18", category_id=9, name="Organic Ancient Foxtail Millet", slug="millets", category_slug="millets",
        price=160.00, unit="kg", original_price=180.00, coop_price=144.00, discount_pct=0,
        image_url=find_product_icon("Foxtail Millets"), quantity=120, manufacture_date="2026-07-14",
        expiry_date="2027-01-14", onboarding_date="2026-07-01", manufacturer_name="Nagamangala Rainfed Farms",
        description="Nutrient-dense ancient foxtail millet grain.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="19", category_id=10, name="Organic Cold Pressed Mustard Oil", slug="oils", category_slug="oils",
        price=320.00, unit="L", original_price=350.00, coop_price=288.00, discount_pct=8,
        image_url=find_product_icon("Mustard Oil"), quantity=75, manufacture_date="2026-07-22",
        expiry_date="2027-07-22", onboarding_date="2026-07-01", manufacturer_name="Challakere Wooden Ghani Mill",
        description="Traditional wooden cold-pressed pure mustard oil.",
        variants=["250mL", "500mL", "1L"]
    ),
]


def get_all_categories() -> List[Category]:
    """Fetch categories from MySQL Category table."""
    db_rows = db_manager.fetch_all_categories_db()
    if not db_rows:
        return FALLBACK_CATEGORIES
    
    categories = []
    for r in db_rows:
        cat_id = r["category_id"]
        name = r["category_name"]
        slug = db_manager.CATEGORY_SLUGS.get(cat_id, name.lower().replace(" ", "-"))
        img = db_manager.CATEGORY_IMAGES.get(cat_id, "assets/images/fruits.jpg")
        categories.append(Category(
            category_id=cat_id,
            name=name,
            slug=slug,
            description=r.get("description") or f"Organic {name}",
            image_url=img
        ))
    return categories


def get_products_by_category_id(category_id: int) -> List[Product]:
    """Fetch products matching category_id directly from MySQL Product table."""
    db_rows = db_manager.fetch_products_by_category_db(category_id)
    if not db_rows:
        return [p for p in FALLBACK_PRODUCTS if p.category_id == category_id]
    
    products = []
    for r in db_rows:
        prod_id = str(r["product_id"])
        cat_id = r["category_id"]
        p_name = r["product_name"]
        price = float(r["price"]) if r["price"] else 0.0
        disc = int(r["discount"]) if r["discount"] else None
        
        # Unit extraction & category enforcement
        unit = get_default_unit_for_category(cat_id, p_name) if cat_id in (1, 2, 3, 4, 5, 6, 7) else (r.get("unit") or get_default_unit_for_category(cat_id, p_name))

        orig_price = round(price / (1 - (disc / 100.0)), 2) if (disc and disc > 0 and disc < 100) else round(price * 1.15, 2) if disc else None
        img_file = find_product_icon(p_name)
        c_slug = db_manager.CATEGORY_SLUGS.get(cat_id, "fruits")
        variants = get_variants_for_unit(unit, cat_id, p_name)

        products.append(Product(
            id=prod_id,
            category_id=cat_id,
            name=p_name,
            slug=p_name.lower().replace(" ", "-"),
            category_slug=c_slug,
            price=price,
            unit=unit,
            original_price=orig_price,
            coop_price=round(price * 0.9, 2),
            discount_pct=disc,
            image_url=img_file,
            variants=variants,
            quantity=r.get("quantity") or 50,
            manufacture_date=str(r.get("manufacture_date") or "2026-07-20"),
            expiry_date=str(r.get("expiry_date") or "2027-07-20"),
            onboarding_date="2026-07-01",
            manufacturer_name="Organic Produce Co-Op",
            farmer_name="Ramakrishnappa",
            farm_location="Organic Belt, Mandya",
            harvest_date=str(r.get("manufacture_date") or "2026-07-20"),
            batch_no=f"OF-BATCH-10{cat_id}",
            description=f"Fresh 100% organic {p_name}."
        ))
    return products


def get_products_by_category(category_slug: str) -> List[Product]:
    """Filter products by category slug or category_id."""
    cats = get_all_categories()
    matched_cat = next((c for c in cats if c.slug == category_slug or str(c.category_id) == str(category_slug)), None)
    if matched_cat:
        return get_products_by_category_id(matched_cat.category_id)
    
    # Try fetching all products if category_slug is 'all'
    if category_slug == "all":
        all_prods = []
        for c in cats:
            all_prods.extend(get_products_by_category_id(c.category_id))
        return all_prods
    return []


CATEGORIES = get_all_categories()
PRODUCTS = get_products_by_category("all")


def get_products_by_tag(tag: str) -> List[Product]:
    all_p = get_products_by_category("all")
    if tag == "all":
        return all_p
    return [p for p in all_p if tag in p.tags]


def get_product_by_id(product_id: str) -> Optional[Product]:
    all_p = get_products_by_category("all")
    return next((p for p in all_p if p.id == str(product_id)), None)


def get_product_by_batch(batch_no: str) -> Optional[Product]:
    all_p = get_products_by_category("all")
    if not batch_no:
        return all_p[0] if all_p else None
    return next((p for p in all_p if hasattr(p, 'batch_no') and p.batch_no.lower() == batch_no.lower()), all_p[0] if all_p else None)


def search_products(query: str) -> List[Product]:
    q = query.lower().strip()
    all_p = get_products_by_category("all")
    if not q:
        return all_p
    return [
        p for p in all_p
        if q in p.name.lower() or q in p.description.lower() or q in p.category_slug.lower()
    ]


def get_bestseller_products() -> List[Product]:
    """Fetch Bestseller products using MySQL Order_Details query or fallback to default bestsellers."""
    db_items = db_manager.fetch_bestsellers_db()
    if db_items:
        prods = []
        for r in db_items:
            existing = get_product_by_id(str(r["product_id"]))
            p_name = r.get("product_name") or "Organic Product"
            mrp = float(r.get("price") or 0.0)
            disc = float(r.get("discount") or 0.0)
            final_price = float(r.get("price_after_discount") if r.get("price_after_discount") is not None else (mrp - disc))
            
            if existing:
                existing.original_price = mrp
                existing.discount_pct = int(disc)
                existing.price = final_price
                prods.append(existing)
            else:
                p_id = str(r["product_id"])
                cat_id = r.get("category_id") or 1
                prods.append(Product(
                    id=p_id,
                    category_id=cat_id,
                    name=p_name,
                    slug=p_name.lower().replace(" ", "-"),
                    category_slug="organic",
                    price=final_price,
                    original_price=mrp,
                    discount_pct=int(disc),
                    image_url=find_product_icon(p_name)
                ))
        return prods

    # Fallback to tagged bestsellers if Order_Details is empty
    return get_products_by_tag("bestseller")


def get_deals_products() -> List[Product]:
    """Fetch Deals products ordered by discount percentage/amount using MySQL query:
    SELECT a.product_name, a.price, a.discount, a.price - a.discount FROM Product a ORDER BY 3 desc LIMIT 10
    """
    db_items = db_manager.fetch_deals_db()
    if db_items:
        prods = []
        for r in db_items:
            existing = get_product_by_id(str(r["product_id"]))
            p_name = r.get("product_name") or "Organic Product"
            mrp = float(r.get("price") or 0.0)
            disc = float(r.get("discount") or 0.0)
            final_price = float(r.get("price_after_discount") if r.get("price_after_discount") is not None else (mrp - disc))
            
            if existing:
                existing.original_price = mrp
                existing.discount_pct = int(disc)
                existing.price = final_price
                prods.append(existing)
            else:
                p_id = str(r["product_id"])
                cat_id = r.get("category_id") or 1
                prods.append(Product(
                    id=p_id,
                    category_id=cat_id,
                    name=p_name,
                    slug=p_name.lower().replace(" ", "-"),
                    category_slug="organic",
                    price=final_price,
                    original_price=mrp,
                    discount_pct=int(disc),
                    image_url=find_product_icon(p_name)
                ))
        return prods

    # Fallback to tagged deals if database query is empty
    return get_products_by_tag("deal")


def get_new_arrivals_products() -> List[Product]:
    """Fetch New Arrivals products ordered by onboarding date using MySQL query:
    SELECT a.product_name, a.price, a.discount, a.price - a.discount FROM Product a ORDER BY onboarding_date desc LIMIT 10
    """
    db_items = db_manager.fetch_new_arrivals_db()
    if db_items:
        prods = []
        for r in db_items:
            existing = get_product_by_id(str(r["product_id"]))
            p_name = r.get("product_name") or "Organic Product"
            mrp = float(r.get("price") or 0.0)
            disc = float(r.get("discount") or 0.0)
            final_price = float(r.get("price_after_discount") if r.get("price_after_discount") is not None else (mrp - disc))
            
            if existing:
                existing.original_price = mrp
                existing.discount_pct = int(disc)
                existing.price = final_price
                prods.append(existing)
            else:
                p_id = str(r["product_id"])
                cat_id = r.get("category_id") or 1
                prods.append(Product(
                    id=p_id,
                    category_id=cat_id,
                    name=p_name,
                    slug=p_name.lower().replace(" ", "-"),
                    category_slug="organic",
                    price=final_price,
                    original_price=mrp,
                    discount_pct=int(disc),
                    image_url=find_product_icon(p_name)
                ))
        return prods

    # Fallback to tagged new arrivals if database query is empty
    return get_products_by_tag("new")

