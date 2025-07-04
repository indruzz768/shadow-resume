#!/usr/bin/env bash
set -o errexit

echo "🔧 Installing Python packages..."
pip install -r requirements.txt

echo "🎨 Building Tailwind styles..."
cd theme/static_src
npm ci
npm run build
cd ../../

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput
