<?php get_header(); the_post(); ?>

<section class="article-hero">
  <div class="wrap">
    <div class="meta">
      <span><?php echo get_the_date('Y.m.d'); ?></span>
      <?php foreach (get_the_category() as $cat) : if ($cat->name !== '未分類') : ?>
      <span class="tag"><?php echo esc_html($cat->name); ?></span>
      <?php endif; endforeach; ?>
    </div>
    <h1><?php the_title(); ?></h1>
    <?php if (has_post_thumbnail()) : ?>
    <div class="article-eyecatch"><?php the_post_thumbnail('full'); ?></div>
    <?php endif; ?>
  </div>
</section>

<div class="article">
  <?php the_content(); ?>

  <div class="cta-inline">
    <div class="lead-s">＼ 交通事故のお悩み、無料で相談できます ／</div>
    <div class="hero-cta">
      <a class="btn btn-line btn-lg" href="https://lin.ee/XPgv3I6" target="_blank" rel="noopener">LINEで予約・無料相談<span class="sub">24時間受付中</span></a>
      <a class="btn btn-tel btn-lg" href="tel:0568901841">0568-90-1841<span class="sub">タップで電話</span></a>
    </div>
  </div>

  <div class="shop-box">
    <div class="head">BTG接骨院 小牧院</div>
    <div class="body">
      <table>
        <tr><th>住所</th><td>〒485-0058 愛知県小牧市小木1丁目112 プローグ小木II 1F</td></tr>
        <tr><th>電話</th><td>0568-90-1841（交通事故は夜20時まで受付）</td></tr>
        <tr><th>窓口負担</th><td>自賠責保険適用で0円</td></tr>
        <tr><th>詳しくは</th><td><a href="https://jiko.sekkotsuin-komaki.com/">交通事故専門サイトへ</a></td></tr>
      </table>
    </div>
  </div>

  <p style="text-align:center;margin-top:2em"><a class="btn btn-outline" href="<?php echo esc_url(home_url('/')); ?>">← ブログ一覧へ戻る</a></p>
</div>

<?php get_footer(); ?>
