<?php get_header(); ?>

<section class="blog-list">
  <div class="wrap">
    <div class="sec-head">
      <span class="en">BLOG</span>
      <h2>交通事故<span class="hl">お役立ちブログ</span></h2>
      <p>事故後の「どうすれば？」を解決する情報を、小牧市の交通事故専門院が発信します。</p>
    </div>
    <div class="blog-grid">
      <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
      <a class="bcard" href="<?php the_permalink(); ?>">
        <?php if (has_post_thumbnail()) : ?>
        <div class="thumb"><?php the_post_thumbnail('large', ['loading' => 'lazy']); ?></div>
        <?php else : ?>
        <div class="thumb noimg">交通事故お役立ちブログ</div>
        <?php endif; ?>
        <div class="body">
          <span class="date"><?php echo get_the_date('Y.m.d'); ?></span>
          <h3><?php the_title(); ?></h3>
          <p><?php echo esc_html(wp_trim_words(get_the_excerpt(), 60, '…')); ?></p>
          <div class="tags">
            <?php foreach (get_the_category() as $cat) : if ($cat->name !== '未分類') : ?>
            <span class="tag"><?php echo esc_html($cat->name); ?></span>
            <?php endif; endforeach; ?>
          </div>
        </div>
      </a>
      <?php endwhile; else : ?>
      <p>記事はまだありません。</p>
      <?php endif; ?>
    </div>
    <?php the_posts_pagination(['prev_text' => '←', 'next_text' => '→']); ?>
    <div class="blog-coming">交通事故・むちうちに関するお役立ち記事を続々更新中です。お楽しみに！</div>
  </div>
</section>

<?php get_footer(); ?>
