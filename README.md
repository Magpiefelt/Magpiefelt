# Magpie Crafts - Wool Felting E-commerce Platform

A comprehensive e-commerce platform for your wool felting and craft business, built with Python/Django and designed to support AI integrations for future projects.

## Features

- **E-commerce Functionality**
  - Product listings with categories for kits, art, and candy
  - Shopping cart and checkout system
  - Stripe payment processing with Canadian GST
  - Order management dashboard
  - Inventory tracking

- **Social Media Integration**
  - Embedded Instagram/TikTok video feeds
  - Newsletter integration
  - Open Graph metadata for social sharing

- **Video Content Embedding**
  - Support for TikTok, Instagram, YouTube videos
  - Local video upload capabilities
  - Video categorization and filtering

- **AI Content Generation**
  - Product description generation
  - Blog post content creation
  - Social media caption generation
  - Review and approval workflow

- **User-Friendly Admin Interface**
  - Intuitive dashboard for all site management
  - One-click actions for common tasks
  - AI content integration

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: TailwindCSS
- **Database**: SQLite (development) / PostgreSQL (production)
- **Payment Processing**: Stripe
- **Media Storage**: AWS S3 (production)
- **AI Integration**: OpenAI API

## Getting Started

### Local Development

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your values
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Start the development server: `python manage.py runserver`

### Deployment

See the [DEPLOYMENT.md](DEPLOYMENT.md) file for detailed deployment instructions to various platforms including Render, Vercel, and AWS.

## Project Structure

- `magpie_crafts/` - Main project settings
- `products/` - Product management app
- `cart/` - Shopping cart functionality
- `orders/` - Order processing and management
- `blog/` - Blog and educational content
- `social/` - Social media integration
- `videos/` - Video content management
- `ai_content/` - AI content generation
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded content

## Customization

The application is designed to be easily customizable:

- Modify templates in the `templates/` directory
- Update styles in the TailwindCSS configuration
- Add new product types by extending the product models
- Create new AI prompt templates in the admin interface

## License

This project is licensed for your exclusive use.

## Acknowledgements

- Built with Django and TailwindCSS
- Payment processing by Stripe
- AI content generation powered by OpenAI
