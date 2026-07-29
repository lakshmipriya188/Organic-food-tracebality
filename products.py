"""Organic Mandya complete product & category data model matching reference images."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Category:
    name: str
    slug: str
    image_url: str
    item_count: int = 24


@dataclass
class Product:
    id: str
    name: str
    slug: str
    category_slug: str
    price: float
    original_price: Optional[float] = None
    coop_price: float = 0.0
    discount_pct: Optional[int] = None
    image_url: str = ""
    variants: List[str] = field(default_factory=lambda: ["500g", "1kg"])
    tags: List[str] = field(default_factory=list)
    rating: float = 4.9
    reviews_count: int = 142
    origin: str = "Mandya Organic Farmer Cooperative"
    lab_cert: str = "NABL Accredited - 100% Pesticide Free"
    description: str = ""


# 16 Reference Categories from Image 2
CATEGORIES = [
    Category(
        name="Staples",
        slug="staples",
        image_url="https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Millets",
        slug="millets",
        image_url="https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Dairy",
        slug="dairy",
        image_url="https://images.unsplash.com/photo-1631451095765-2c91616fc9e6?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Cold Pressed Oils",
        slug="cold-pressed-oils",
        image_url="https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Dry Fruits",
        slug="dry-fruits",
        image_url="https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Spices & Masalas",
        slug="spices-masalas",
        image_url="https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Beverages",
        slug="beverages",
        image_url="https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Snacks",
        slug="snacks",
        image_url="https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Sweets",
        slug="sweets",
        image_url="https://images.unsplash.com/photo-1599785209707-a456fc1337bb?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Sweeteners",
        slug="sweeteners",
        image_url="https://images.unsplash.com/photo-1587049352847-4a222e784d38?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Bakery",
        slug="bakery",
        image_url="https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Ready to Cook",
        slug="ready-to-cook",
        image_url="https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Edibles",
        slug="edibles",
        image_url="https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Fruits & Vegetables",
        slug="fruits-vegetables",
        image_url="https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Personal Care",
        slug="personal-care",
        image_url="https://images.unsplash.com/photo-1608248597379-e07439546278?w=400&auto=format&fit=crop&q=80"
    ),
    Category(
        name="Home Essentials",
        slug="home-essentials",
        image_url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400&auto=format&fit=crop&q=80"
    ),
]


# Exact Products from Reference Image 3 and Image 1
PRODUCTS = [
    Product(
        id="prod_rajmudi",
        name="Organic Rajmudi Rice (Rajamudi) - Karnataka's Heritage Red Rice",
        slug="organic-rajmudi-rice",
        category_slug="staples",
        price=152.00,
        original_price=None,
        coop_price=136.80,
        discount_pct=None,
        image_url="https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&auto=format&fit=crop&q=80",
        variants=["1kg", "5kg", "25kg"],
        tags=["bestseller"],
        origin="Mysuru-Mandya Royal Heritage Farms",
        description="Traditional royal rice once favored by the Maharajas of Mysore, unpolished and packed with fiber and zinc."
    ),
    Product(
        id="prod_a2ghee",
        name="A2 Ghee - Desi Cow Ghee (Bilona Method)",
        slug="a2-desi-cow-ghee",
        category_slug="dairy",
        price=625.50,
        original_price=695.00,
        coop_price=562.95,
        discount_pct=10,
        image_url="https://images.unsplash.com/photo-1631451095765-2c91616fc9e6?w=500&auto=format&fit=crop&q=80",
        variants=["275ml", "500ml", "1L"],
        tags=["bestseller", "deal"],
        origin="Mandya Cow Sanctuary & Dairy Cooperative",
        description="Handmade in small batches using traditional Bilona two-way churn method from A2 Hallikar & Gir cows."
    ),
    Product(
        id="prod_groundnutoil",
        name="Organic Cold Pressed Groundnut Oil (Peanut Oil)",
        slug="cold-pressed-groundnut-oil",
        category_slug="cold-pressed-oils",
        price=494.00,
        original_price=500.00,
        coop_price=444.60,
        discount_pct=1,
        image_url="https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&auto=format&fit=crop&q=80",
        variants=["1L", "5L"],
        tags=["bestseller", "deal"],
        origin="Challakere Peanut Farms, Karnataka",
        description="Extracted in wooden Ghani at slow RPM to preserve heart-healthy monounsaturated fatty acids and natural aroma."
    ),
    Product(
        id="prod_toordal",
        name="Organic Toor Dal (Tuvar Dal / Arhar Dal) — Unpolished",
        slug="organic-toor-dal",
        category_slug="staples",
        price=182.00,
        original_price=None,
        coop_price=163.80,
        discount_pct=None,
        image_url="https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?w=500&auto=format&fit=crop&q=80",
        variants=["500g", "1kg"],
        tags=["bestseller"],
        origin="Gulbarga Organic Pulse Growers",
        description="Native seed unpolished protein pulse grown naturally without chemical pesticides or artificial yellow dye."
    ),
    Product(
        id="prod_moongdal",
        name="Farm-Fresh Organic Moong Dal",
        slug="organic-moong-dal",
        category_slug="staples",
        price=162.00,
        original_price=None,
        coop_price=145.80,
        discount_pct=None,
        image_url="https://images.unsplash.com/photo-1585992227182-3d772c918e97?w=500&auto=format&fit=crop&q=80",
        variants=["500g", "1kg"],
        tags=["bestseller"],
        origin="Raichur Farmer Producer Co-op",
        description="Easy-to-digest split yellow moong dal unpolished and solar-dried to lock in essential minerals."
    ),

    # Millets from Image 1
    Product(
        id="prod_foxtail",
        name="Single-Origin Organic Foxtail Millet (Navane)",
        slug="foxtail-millet",
        category_slug="millets",
        price=175.00,
        original_price=190.00,
        coop_price=157.50,
        discount_pct=8,
        image_url="https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=500&auto=format&fit=crop&q=80",
        variants=["500g", "1kg"],
        tags=["new", "deal"],
        origin="Mandya Millet Collective",
        description="Low GI ancient grain rich in calcium, iron, and fiber."
    ),
    Product(
        id="prod_browntop",
        name="Native Organic Browntop Millet (Kadu Baragu)",
        slug="browntop-millet",
        category_slug="millets",
        price=220.00,
        original_price=None,
        coop_price=198.00,
        discount_pct=None,
        image_url="https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&auto=format&fit=crop&q=80",
        variants=["500g", "1kg"],
        tags=["new"],
        origin="Tumakuru Rainfed Farms",
        description="Highest dietary fiber content (12.5%) among all millets, ideal for diabetic management."
    ),
    Product(
        id="prod_ragi",
        name="Whole Organic Ragi (Finger Millet / Eleusine coracana)",
        slug="organic-ragi",
        category_slug="millets",
        price=110.00,
        original_price=None,
        coop_price=99.00,
        discount_pct=None,
        image_url="https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&auto=format&fit=crop&q=80",
        variants=["1kg", "5kg"],
        tags=["bestseller"],
        origin="Mandya Heartlands",
        description="Rich source of natural calcium (344mg per 100g), milled fresh daily."
    ),
    Product(
        id="prod_proso",
        name="Single-Origin Organic Proso Millet (Baragu)",
        slug="proso-millet",
        category_slug="millets",
        price=165.00,
        original_price=None,
        coop_price=148.50,
        discount_pct=None,
        image_url="https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=500&auto=format&fit=crop&q=80",
        variants=["500g", "1kg"],
        tags=["new"],
        origin="Chitradurga Millet Belt",
        description="High protein, nervous-system supporting millet with high magnesium and phosphorus."
    ),
]


def get_products_by_category(category_slug: str) -> List[Product]:
    """Filter products by category slug."""
    if category_slug == "all":
        return PRODUCTS
    return [p for p in PRODUCTS if p.category_slug == category_slug]


def get_products_by_tag(tag: str) -> List[Product]:
    """Filter products by tag (e.g. bestseller, deal, new)."""
    if tag == "all":
        return PRODUCTS
    return [p for p in PRODUCTS if tag in p.tags]


def get_product_by_id(product_id: str) -> Optional[Product]:
    """Find product by unique ID."""
    return next((p for p in PRODUCTS if p.id == product_id), None)


def get_product_by_batch(batch_no: str) -> Optional[Product]:
    """Find product by batch number."""
    if not batch_no:
        return PRODUCTS[0]
    return next((p for p in PRODUCTS if hasattr(p, 'batch_no') and p.batch_no.lower() == batch_no.lower()), PRODUCTS[0])


def search_products(query: str) -> List[Product]:
    """Search products by name, description, or origin."""
    q = query.lower().strip()
    if not q:
        return PRODUCTS
    return [
        p for p in PRODUCTS
        if q in p.name.lower() or q in p.description.lower() or q in p.category_slug.lower()
    ]
