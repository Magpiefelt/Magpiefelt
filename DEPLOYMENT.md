# Deployment Guide for Magpie Crafts

This guide will help you deploy your Magpie Crafts wool felting e-commerce application to various hosting platforms. We've prepared the application to be easily deployable to platforms like Render, Vercel, or AWS as you mentioned in your requirements.

## Prerequisites

Before deploying, make sure you have:

1. Your domain name ready
2. A Stripe account for payment processing
3. An OpenAI API key (for AI content generation features)
4. (Optional) An AWS account if you want to use S3 for media storage

## Deployment Options

### Option 1: Render

[Render](https://render.com/) is a unified platform to build and run all your apps and websites with free SSL, global CDN, private networks, and auto deploys from Git.

1. **Create a Render account** if you don't have one already
2. **Create a new Web Service**
   - Connect your GitHub/GitLab repository or upload the code
   - Select "Python" as the environment
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn magpie_crafts.wsgi:application`
3. **Add environment variables**
   - Copy all variables from `.env.example` and add them to Render's environment variables section
   - Make sure to set `DEBUG=False` and `ALLOWED_HOSTS` to your domain
4. **Set up a PostgreSQL database**
   - Create a PostgreSQL database in Render
   - Add the database URL to your environment variables as `DATABASE_URL`
5. **Connect your domain**
   - In the Render dashboard, go to your web service settings
   - Navigate to "Custom Domains"
   - Add your domain and follow the instructions to set up DNS

### Option 2: Vercel

[Vercel](https://vercel.com/) is a platform for frontend frameworks and static sites, but it can also host Django applications.

1. **Install Vercel CLI**: `npm i -g vercel`
2. **Create a `vercel.json` file** in your project root:
   ```json
   {
     "builds": [
       {
         "src": "magpie_crafts/wsgi.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "magpie_crafts/wsgi.py"
       }
     ]
   }
   ```
3. **Deploy using Vercel CLI**: Run `vercel` in your project directory
4. **Set environment variables** in the Vercel dashboard
5. **Connect your domain** in the Vercel dashboard

### Option 3: AWS Elastic Beanstalk

For a more scalable solution, AWS Elastic Beanstalk is a good option:

1. **Install the AWS CLI and EB CLI**
2. **Initialize your EB application**: `eb init`
3. **Create an environment**: `eb create`
4. **Configure environment variables** using the AWS console
5. **Deploy your application**: `eb deploy`
6. **Set up your domain** using AWS Route 53

## Setting Up Environment Variables

Regardless of which platform you choose, you'll need to set up environment variables:

1. Copy the `.env.example` file to `.env` for local development
2. For production, add these variables to your hosting platform's environment variables section
3. Make sure to set `DEBUG=False` for production
4. Add your domain to `ALLOWED_HOSTS`

## Database Migration

After deploying, you'll need to run database migrations:

```
python manage.py migrate
```

Most platforms allow you to run this command through their console/terminal feature.

## Creating a Superuser

To access the admin interface, create a superuser:

```
python manage.py createsuperuser
```

Follow the prompts to create your admin username and password.

## Setting Up Media Storage

For production, we recommend using AWS S3 for media storage:

1. Create an S3 bucket in your AWS account
2. Set the appropriate permissions (make it publicly readable)
3. Create an IAM user with access to the bucket
4. Set the following environment variables:
   - `USE_S3=True`
   - `AWS_ACCESS_KEY_ID=your-access-key`
   - `AWS_SECRET_ACCESS_KEY=your-secret-key`
   - `AWS_STORAGE_BUCKET_NAME=your-bucket-name`

## Setting Up Stripe

1. Add your Stripe public and secret keys to the environment variables
2. Set up a webhook in your Stripe dashboard pointing to `https://yourdomain.com/orders/webhook/`
3. Add the webhook secret to your environment variables

## Setting Up OpenAI API

1. Add your OpenAI API key to the environment variables
2. Test the AI content generation features from the admin dashboard

## Maintenance and Updates

To update your application:

1. Make changes to your code locally
2. Test thoroughly
3. Commit and push to your repository
4. Your hosting platform should automatically deploy the changes (if set up for auto-deploy)

## Troubleshooting

If you encounter issues during deployment:

1. Check the logs provided by your hosting platform
2. Ensure all environment variables are set correctly
3. Verify that database migrations have run successfully
4. Check that static files are being served correctly

## Need Help?

If you need assistance with deployment, feel free to:

1. Refer to the documentation of your chosen hosting platform
2. Reach out to a developer for help with the technical aspects
3. Consider using a managed hosting service that specializes in Django applications

Good luck with your wool felting e-commerce business!
