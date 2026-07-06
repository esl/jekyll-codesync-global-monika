# Sass (via jekyll-sass-converter 1.x) reads files as US-ASCII unless the
# locale is UTF-8, so force one for all recipes.
export LC_ALL = en_US.UTF-8
export LANG = en_US.UTF-8

serve:
	bundle exec jekyll serve

build:
	bundle exec jekyll build

install:
	gem install bundler
	bundler update --bundler
