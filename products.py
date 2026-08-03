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
    - Solid items: kg or g
    - Liquid items: L (Litre)
    """
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
    if category_id in (6, 8) or any(k in p_lower for k in ["powder", "spice", "cardamom", "clove", "cinnamon", "butter", "cheese", "yogurt", "cream"]):
        return "g"
        
    return "kg"


def get_variants_for_unit(unit: str, category_id: int = 1, product_name: str = "") -> List[str]:
    """Return standard 250, 500, and 1 measures formatted for liquid (L/mL) vs solid (g/kg)."""
    p_lower = product_name.lower()
    u = unit.lower().strip()
    
    is_liquid = u in ("l", "litre", "1l", "ml") or category_id in (7, 10) or any(k in p_lower for k in ["oil", "milk", "juice", "water", "ghee", "buttermilk", "beverage"])
    if is_liquid and not ("tea" in p_lower or "coffee" in p_lower):
        return ["250mL", "500mL", "1L"]
    else:
        return ["250g", "500g", "1kg"]


def find_product_icon(product_name: str) -> str:
    """Find corresponding product image icon inside product_icons directory."""
    icon_dir = "product_icons"
    if not os.path.exists(icon_dir):
        return "assets/images/fruits.jpg"

    clean_name = (
        product_name.replace("Organic ", "")
        .replace("Fresh ", "")
        .replace("Pure ", "")
        .replace("Ancient ", "")
        .replace("Cold Pressed ", "")
        .replace("Native ", "")
        .replace("Premium ", "")
        .strip()
    )

    files = os.listdir(icon_dir)
    candidates = [product_name.replace(" ", "_"), clean_name.replace(" ", "_")]

    # 1. Exact match (case insensitive)
    for c in candidates:
        for f in files:
            name_no_ext = os.path.splitext(f)[0]
            if c.lower() == name_no_ext.lower():
                return f"{icon_dir}/{f}"

    # 2. Substring match
    for c in candidates:
        for f in files:
            name_no_ext = os.path.splitext(f)[0]
            if c.lower() in name_no_ext.lower() or name_no_ext.lower() in c.lower():
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

# Default static fallback products with category-specific units and measures (250, 500, 1)
FALLBACK_PRODUCTS = [
    Product(
        id="1", category_id=1, name="Organic Fresh Fruits", slug="fruits", category_slug="fruits",
        price=120.00, unit="kg", original_price=140.00, coop_price=108.00, discount_pct=14,
        image_url=find_product_icon("Apple"), quantity=50, manufacture_date="2026-07-20",
        expiry_date="2026-08-05", onboarding_date="2026-07-01", manufacturer_name="Mandya Organic Fruit Orchards",
        description="Farm-fresh handpicked seasonal organic fruits grown without synthetic pesticides.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="2", category_id=2, name="Organic Farm Vegetables", slug="vegetables", category_slug="vegetables",
        price=85.00, unit="kg", original_price=95.00, coop_price=76.50, discount_pct=10,
        image_url=find_product_icon("Tomato"), quantity=100, manufacture_date="2026-07-25",
        expiry_date="2026-08-02", onboarding_date="2026-07-01", manufacturer_name="Maddur Riverbank Farms",
        description="Crisp naturally grown farm vegetables rich in essential nutrients.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="3", category_id=3, name="Organic Whole Grains", slug="grains", category_slug="grains",
        price=150.00, unit="kg", original_price=175.00, coop_price=135.00, discount_pct=0,
        image_url=find_product_icon("Brown Rice"), quantity=200, manufacture_date="2026-07-10",
        expiry_date="2027-07-10", onboarding_date="2026-07-01", manufacturer_name="Mysuru Heritage Paddy Farms",
        description="Unpolished traditional whole grains packed with natural fiber and nutrients.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="4", category_id=4, name="Organic Native Pulses", slug="pulses", category_slug="pulses",
        price=180.00, unit="kg", original_price=200.00, coop_price=162.00, discount_pct=10,
        image_url=find_product_icon("Toor Dal"), quantity=150, manufacture_date="2026-07-12",
        expiry_date="2027-01-12", onboarding_date="2026-07-01", manufacturer_name="Kalaburagi Pulse Collective",
        description="Sun-dried protein-dense native organic pulses.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="5", category_id=5, name="Organic Pure A2 Milk", slug="dairy", category_slug="dairy",
        price=95.00, unit="L", original_price=110.00, coop_price=85.50, discount_pct=0,
        image_url=find_product_icon("Milk"), quantity=40, manufacture_date="2026-07-28",
        expiry_date="2026-07-31", onboarding_date="2026-07-01", manufacturer_name="Pandavapura Bilona Dairy",
        description="Pure unpasteurized fresh A2 Desi Cow milk.",
        variants=["250mL", "500mL", "1L"]
    ),
    Product(
        id="6", category_id=6, name="Organic Aromatic Spices", slug="spices", category_slug="spices",
        price=210.00, unit="g", original_price=230.00, coop_price=189.00, discount_pct=8,
        image_url=find_product_icon("Turmeric Powder"), quantity=80, manufacture_date="2026-07-05",
        expiry_date="2027-07-05", onboarding_date="2026-07-01", manufacturer_name="Sirsi Spice Hills Garden",
        description="Aromatic whole organic spices harvested from Western Ghats.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="7", category_id=7, name="Organic Herbal Beverage", slug="beverages", category_slug="beverages",
        price=135.00, unit="L", original_price=150.00, coop_price=121.50, discount_pct=0,
        image_url=find_product_icon("Herbal Tea"), quantity=60, manufacture_date="2026-07-18",
        expiry_date="2026-10-18", onboarding_date="2026-07-01", manufacturer_name="Chikmagalur Herbal Valley",
        description="Revitalizing natural organic herbal drink bottled fresh.",
        variants=["250mL", "500mL", "1L"]
    ),
    Product(
        id="8", category_id=8, name="Organic Premium Almonds", slug="dry-fruits", category_slug="dry-fruits",
        price=450.00, unit="g", original_price=500.00, coop_price=405.00, discount_pct=10,
        image_url=find_product_icon("Almonds"), quantity=90, manufacture_date="2026-07-08",
        expiry_date="2027-07-08", onboarding_date="2026-07-01", manufacturer_name="Kolar Organic Nut Growers",
        description="Premium crunch raw organic almonds rich in healthy fats.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="9", category_id=9, name="Organic Ancient Foxtail Millet", slug="millets", category_slug="millets",
        price=160.00, unit="kg", original_price=180.00, coop_price=144.00, discount_pct=0,
        image_url=find_product_icon("Foxtail Millets"), quantity=120, manufacture_date="2026-07-14",
        expiry_date="2027-01-14", onboarding_date="2026-07-01", manufacturer_name="Nagamangala Rainfed Farms",
        description="Nutrient-dense ancient foxtail millet grain.",
        variants=["250g", "500g", "1kg"]
    ),
    Product(
        id="10", category_id=10, name="Organic Cold Pressed Mustard Oil", slug="oils", category_slug="oils",
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
        
        # Unit extraction & fallback
        unit = r.get("unit") or get_default_unit_for_category(cat_id, p_name)

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
            onboarding_date=str(r.get("onboarding_date") or "2026-07-01"),
            manufacturer_name=r.get("manufacturer_name") or "Organic Produce Co-Op",
            farmer_name=r.get("manufacturer_name") or "Ramakrishnappa",
            farm_location="Organic Belt, Mandya",
            harvest_date=str(r.get("manufacture_date") or "2026-07-20"),
            batch_no=f"OF-BATCH-10{cat_id}",
            description=f"Fresh 100% organic {p_name} supplied by {r.get('manufacturer_name', 'Organic Farms')}."
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
                    image_url=f"product_icons/prod_{p_id}.png"
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
                    image_url=f"product_icons/prod_{p_id}.png"
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
                    image_url=f"product_icons/prod_{p_id}.png"
                ))
        return prods

    # Fallback to tagged new arrivals if database query is empty
    return get_products_by_tag("new")

