from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

app = Flask(__name__)

DOOR_CONFIG = [
    {
        "slug": "singledoors",
        "name": "Single Doors",
        "category": "doors",
        "summary": "Secure composite entrance doors that combine kerb appeal with everyday durability.",
        "description": "Upgrade your home's security and kerb appeal with our high-performance composite front doors. Built with a robust timber or steel-reinforced core and advanced GRP skins, these doors offer exceptional durability, insulation, and weather resistance.",
        "image_folder": "doors/singledoors",
        "features": [
            "Multi-point locking for maximum security",
            "Wide range of colours and woodgrain finishes",
            "Excellent thermal efficiency",
            "Low maintenance and long-lasting performance"
        ],
        "highlight_features": [
            "Multi-point locking for maximum security",
            "Excellent thermal efficiency"
        ],
        "select_value": "Doors",
    },
    {
        "slug": "crittalldoors",
        "name": "Crittall Doors",
        "category": "doors",
        "summary": "Modern steel-look glazing with ultra-slim sightlines and industrial-inspired grid patterns.",
        "description": "Stylish steel-look doors with slim frames and grid glazing, designed to bring maximum light and a modern industrial finish to any space.",
        "image_folder": "doors/crittalldoors",
        "features": [
            "Ultra-slim sightlines",
            "Modern industrial grid design",
            "Strong steel or aluminium build",
            "High natural light flow"
        ],
        "highlight_features": [
            "Ultra-slim sightlines",
            "Modern industrial grid design"
        ],
        "select_value": "Doors",
    },
    {
        "slug": "frenchdoors",
        "name": "French Doors",
        "category": "doors",
        "summary": "Classic double doors that suit traditional and contemporary homes alike.",
        "description": "Classic and stylish, French doors bring a touch of elegance to any home.",
        "image_folder": "doors/frenchdoors",
        "features": [
            "Twin-door opening for ventilation",
            "Timeless design for traditional and modern homes",
            "Secure multi-point locking",
            "Energy-efficient glazing options"
        ],
        "highlight_features": [
            "Twin-door opening for ventilation",
            "Secure multi-point locking"
        ],
        "select_value": "Doors",
    },
    {
        "slug": "slidingdoors",
        "name": "Sliding Doors",
        "category": "doors",
        "summary": "Large glass panels and effortless glide mechanisms that frame garden views.",
        "description": "Our smooth and sleek sliding doors are perfect for creating wide, uninterrupted views of your outdoor space.",
        "image_folder": "doors/slidingdoors",
        "features": [
            "Effortless sliding mechanism",
            "Large glass panels for maximum natural light",
            "Energy-efficient double or triple glazing",
            "Ideal for patios, gardens, and balconies"
        ],
        "highlight_features": [
            "Effortless sliding mechanism",
            "Large glass panels for maximum natural light"
        ],
        "select_value": "Doors",
    },
    {
        "slug": "bifoldingdoors",
        "name": "Bi-folding Doors",
        "category": "doors",
        "summary": "Open-plan living solutions that stack panels neatly for seamless indoor-outdoor flows.",
        "description": "Transform your living space with our modern bi-folding doors, designed to open up entire walls and create seamless indoor-outdoor living.",
        "image_folder": "doors/bifoldingdoors",
        "features": [
            "Slim aluminium frames",
            "Flexible opening options",
            "High thermal insulation",
            "Secure locking and enhanced weather resistance"
        ],
        "highlight_features": [
            "Slim aluminium frames",
            "Flexible opening options"
        ],
        "select_value": "Doors",
    },
]

WINDOW_CONFIG = [
    {
        "slug": "sashwindows",
        "name": "Sash Windows",
        "category": "windows",
        "summary": "Classic vertical sliding windows that suit heritage-style and period homes.",
        "description": "Our sash windows combine classic charm with modern performance, perfect for heritage-style homes.",
        "image_folder": "windows/sashwindows",
        "features": [
            "Smooth vertical sliding system",
            "Traditional aesthetics",
            "High-quality draught proofing",
            "Low maintenance uPVC or aluminium options",
        ],
        "highlight_features": [
            "Smooth vertical sliding system",
            "High-quality draught proofing",
        ],
        "select_value": "Windows",
    },
    {
        "slug": "casementwindows",
        "name": "Casement Windows",
        "category": "windows",
        "summary": "Versatile outward-opening windows that provide excellent airflow and energy performance.",
        "description": "Casement windows offer excellent airflow and versatility with their outward-opening design.",
        "image_folder": "windows/casementwindows",
        "features": [
            "Highly energy-efficient seals",
            "Multiple opening styles",
            "Secure hinge and locking systems",
            "Suitable for all property types",
        ],
        "highlight_features": [
            "Highly energy-efficient seals",
            "Secure hinge and locking systems",
        ],
        "select_value": "Windows",
    },
    {
        "slug": "heritagewindows",
        "name": "Heritage Windows",
        "category": "windows",
        "summary": "Traditional-look windows for conservation areas and character properties.",
        "description": "Designed to replicate traditional timber styles, our heritage windows are ideal for conservation areas or character homes.",
        "image_folder": "windows/heritagewindows",
        "features": [
            "Authentic sightlines",
            "Slim frames",
            "Superior insulation",
            "Customisable colours and finishes",
        ],
        "highlight_features": [
            "Authentic sightlines",
            "Slim frames",
        ],
        "select_value": "Windows",
    },
    {
        "slug": "baywindows",
        "name": "Bay Windows",
        "category": "windows",
        "summary": "Projecting window bays that create extra space and invite more natural light in.",
        "description": "Create a spacious, light-filled feature in your home with our custom bay windows.",
        "image_folder": "windows/baywindows",
        "features": [
            "Expands room space outward",
            "Enhances natural light",
            "Stylish and energy-efficient",
            "Custom configurations available",
        ],
        "highlight_features": [
            "Expands room space outward",
            "Enhances natural light",
        ],
        "select_value": "Windows",
    },
    {
        "slug": "flushwindows",
        "name": "Flush Windows",
        "category": "windows",
        "summary": "Sleek, modern windows where the sash sits perfectly flush within the outer frame.",
        "description": "Sleek, modern windows with sash frames that sit perfectly flush within the outer frame, offering a clean, minimalist, and timber-style appearance.",
        "image_folder": "windows/flushwindows",
        "features": [
            "Smooth, flush-fitting sash design",
            "Slim, clean sightlines",
            "Modern or traditional timber-look finish",
            "Low-maintenance uPVC or aluminium options",
        ],
        "highlight_features": [
            "Smooth, flush-fitting sash design",
            "Slim, clean sightlines",
        ],
        "select_value": "Windows",
    },
]

ROOFLIGHT_CONFIG = [
    {
        "slug": "slimrooflight",
        "name": "Slim Rooflights",
        "category": "rooflights",
        "summary": "Ultra-slim framed roof lanterns that maximise daylight with minimal sightlines.",
        "description": "Ultra-slim framed roof lanterns designed to maximise daylight with modern minimal sightlines and superior thermal performance.",
        "image_folder": "rooflight/slimrooflight",
        "features": [
            "Super-slim aluminium profiles",
            "Maximum natural light entry",
            "Contemporary minimal design",
            "High thermal efficiency",
            "Ideal for kitchens, extensions & flat roofs",
        ],
        "highlight_features": [
            "Super-slim aluminium profiles",
            "Maximum natural light entry",
        ],
        "select_value": "Rooflights",
    },
    {
        "slug": "pyramidrooflight",
        "name": "Pyramid Rooflights",
        "category": "rooflights",
        "summary": "Four-sided architectural roof lanterns with balanced daylight and strong structure.",
        "description": "Pyramid sky lanterns: a four-sided architectural roof lantern offering balanced daylight, elegant aesthetics, and excellent structural stability.",
        "image_folder": "rooflight/pyramidrooflight",
        "features": [
            "Symmetrical pyramid design",
            "360° natural light flow",
            "Strong and weather-resistant frame",
            "Excellent insulation performance",
            "Suitable for flat and pitched roofs",
        ],
        "highlight_features": [
            "Symmetrical pyramid design",
            "360° natural light flow",
        ],
        "select_value": "Rooflights",
    },
]

CONSERVATORY_CONFIG = [
    {
        "slug": "conservatories",
        "name": "Conservatories",
        "category": "conservatories",
        "summary": "Light-filled extensions that add usable space, comfort, and value to your home.",
        "description": "A beautiful light-filled extension that transforms your home with extra space, warmth, and year-round comfort.",
        "image_folder": "conservatories",
        "features": [
            "Creates a bright, relaxing space for dining, lounging, or hosting",
            "Floods your home with natural light",
            "Modern thermal glazing keeps it warm in winter, cool in summer",
            "Low-maintenance uPVC or aluminium frames",
            "Custom designs: Victorian, Edwardian, Lean-to & bespoke styles",
        ],
        "highlight_features": [
            "Creates a bright, relaxing space",
            "Modern thermal glazing for year-round comfort",
        ],
        "select_value": "Conservatories",
    }
]


@app.context_processor
def inject_globals():
    return {"current_year": datetime.now().year}


def _load_images(relative_folder: str):
    """Load image filenames from a folder relative to static/images."""
    directory = os.path.join(app.static_folder, 'images', *relative_folder.split('/'))
    if not os.path.isdir(directory):
        return []

    files = sorted([
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and 
        f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
    ])
    return [f"{relative_folder.rstrip('/')}/{filename}" for filename in files]


def _get_door_type(slug: str):
    """Get door configuration by slug with images."""
    for config in DOOR_CONFIG:
        if config["slug"] == slug:
            door = config.copy()
            door["images"] = _load_images(config["image_folder"])
            return door
    return None


def _get_all_doors():
    """Get all door configurations with images."""
    return [_get_door_type(config["slug"]) for config in DOOR_CONFIG]


def _get_window_type(slug: str):
    """Get window configuration by slug with images."""
    for config in WINDOW_CONFIG:
        if config["slug"] == slug:
            win = config.copy()
            win["images"] = _load_images(config["image_folder"])
            return win
    return None


def _get_rooflight_type(slug: str):
    """Get rooflight configuration by slug with images."""
    for config in ROOFLIGHT_CONFIG:
        if config["slug"] == slug:
            roof = config.copy()
            roof["images"] = _load_images(config["image_folder"])
            return roof
    return None


def _get_conservatory_type(slug: str):
    """Get conservatory configuration by slug with images."""
    for config in CONSERVATORY_CONFIG:
        if config["slug"] == slug:
            cons = config.copy()
            cons["images"] = _load_images(config["image_folder"])
            return cons
    return None


def _get_variant(slug: str):
    """Get any product variant by slug."""
    for getter in (_get_door_type, _get_window_type, _get_rooflight_type, _get_conservatory_type):
        variant = getter(slug)
        if variant:
            return variant
    return None


def _feedback_redirect(flag: str):
    """Redirect back to the referring page with a status flag appended."""
    target = request.referrer or url_for('home')
    parsed = urlparse(target)

    # Handle internal redirects
    if not parsed.netloc:
        path = parsed.path or url_for('home')
        separator = '&' if '?' in path else '?'
        return redirect(f"{path}{separator}{flag}=true")

    # Handle external/full URL redirects
    query_params = dict(parse_qsl(parsed.query))
    query_params[flag] = "true"
    new_query = urlencode(query_params)
    redirect_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return redirect(redirect_url)


@app.route('/')
def home():
    """Home page route."""
    return render_template('home.html', active_page='home')


@app.route('/products')
def products():
    """Products overview page showing all categories."""
    door_types = _get_all_doors()
    window_types = [_get_window_type(cfg["slug"]) for cfg in WINDOW_CONFIG]
    rooflight_types = [_get_rooflight_type(cfg["slug"]) for cfg in ROOFLIGHT_CONFIG]
    conservatory_types = [_get_conservatory_type(cfg["slug"]) for cfg in CONSERVATORY_CONFIG]
    return render_template(
        'products.html',
        door_types=door_types,
        window_types=window_types,
        rooflight_types=rooflight_types,
        conservatory_types=conservatory_types,
        active_page='products',
    )


@app.route('/products/<slug>')
def product_detail(slug):
    """Individual product detail page."""
    product = _get_variant(slug)
    if not product:
        abort(404)
    return render_template('product_detail.html', door=product, active_page='products')


@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html', active_page='about')


@app.route('/reviews')
def reviews():
    """Reviews page route."""
    return render_template('reviews.html', active_page='reviews')


@app.route('/contact')
def contact():
    """Contact page route."""
    return render_template('contact.html', active_page='contact')

@app.route('/send_enquiry')
def send_enquiry():
    pass



if __name__ == '__main__':
    app.run(debug=True)