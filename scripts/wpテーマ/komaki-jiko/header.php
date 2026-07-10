<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<div class="progress" id="progress"></div>

<header>
  <div class="wrap hbar">
    <a href="https://jiko.sekkotsuin-komaki.com/" class="logo">
      <span class="mark">BTG</span>
      <span>BTG接骨院 小牧院<small>交通事故・むち打ち専門サイト</small></span>
    </a>
    <nav class="hnav">
      <a class="navlink" href="https://jiko.sekkotsuin-komaki.com/index.html#symptoms">症状ページ</a>
      <a class="navlink" href="https://jiko.sekkotsuin-komaki.com/事例/index.html">事故の実例</a>
      <a class="navlink" href="https://jiko.sekkotsuin-komaki.com/院の雰囲気.html">院の雰囲気</a>
      <a class="navlink" href="https://jiko.sekkotsuin-komaki.com/index.html#sim">慰謝料計算</a>
      <a class="navlink" href="https://jiko.sekkotsuin-komaki.com/index.html#access">アクセス</a>
      <a class="navlink" href="<?php echo esc_url(home_url('/')); ?>">ブログ</a>
    </nav>
    <div class="hcta">
      <a class="btn btn-line" href="https://lin.ee/XPgv3I6" target="_blank" rel="noopener">LINEで予約</a>
      <a class="btn btn-tel" href="tel:0568901841">電話する</a>
    </div>
    <button class="burger" aria-label="メニュー" id="burger">☰</button>
  </div>
</header>

<div class="mobile-nav" id="mnav">
  <button class="close" id="mclose" aria-label="閉じる">✕</button>
  <a href="https://jiko.sekkotsuin-komaki.com/">トップページ</a>
  <a href="https://jiko.sekkotsuin-komaki.com/index.html#symptoms">症状別ページ</a>
  <a href="https://jiko.sekkotsuin-komaki.com/事例/index.html">事故の実例</a>
  <a href="https://jiko.sekkotsuin-komaki.com/院の雰囲気.html">院の雰囲気</a>
  <a href="https://jiko.sekkotsuin-komaki.com/index.html#sim">慰謝料計算</a>
  <a href="<?php echo esc_url(home_url('/')); ?>">ブログ</a>
  <a href="https://jiko.sekkotsuin-komaki.com/index.html#access">アクセス</a>
  <a class="btn btn-line" href="https://lin.ee/XPgv3I6" target="_blank" rel="noopener">LINEで予約・相談</a>
</div>

<nav class="breadcrumb" aria-label="パンくず">
  <a href="https://jiko.sekkotsuin-komaki.com/">トップ</a><span><?php if (is_single()) : ?><a href="<?php echo esc_url(home_url('/')); ?>">ブログ</a></span><span><?php the_title(); ?><?php else : ?>ブログ<?php endif; ?></span>
</nav>
