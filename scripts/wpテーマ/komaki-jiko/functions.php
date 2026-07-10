<?php
add_theme_support('title-tag');
add_theme_support('post-thumbnails');
add_theme_support('automatic-feed-links');

function komaki_jiko_assets() {
  $site = 'https://jiko.sekkotsuin-komaki.com';
  wp_enqueue_style('site-base', $site . '/assets/css/style.css', [], '1.0');
  wp_enqueue_style('site-sym',  $site . '/assets/css/症状ページ.css', ['site-base'], '1.0');
  wp_enqueue_style('site-blog', $site . '/assets/css/ブログ.css', ['site-sym'], '1.0');
  wp_enqueue_style('theme', get_stylesheet_uri(), ['site-blog'], '1.0');
  wp_enqueue_script('site-main', $site . '/assets/js/main.js', [], '1.0', true);
}
add_action('wp_enqueue_scripts', 'komaki_jiko_assets');

// 抜粋を短く
add_filter('excerpt_length', function(){ return 60; });
add_filter('excerpt_more', function(){ return '…'; });
