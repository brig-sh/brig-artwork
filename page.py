"""Build the brig/hull identity review page with every asset inlined."""
import base64
import os

A = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(A, 'identity.html')


def uri(rel):
    with open(os.path.join(A, rel), 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    mime = 'image/svg+xml' if rel.endswith('.svg') else 'image/png'
    return f'data:{mime};base64,{b64}'


S = {n: uri(f'svg/{n}.svg') for n in [
    'brig-avatar', 'hull-avatar', 'brig-mark-on-dark', 'brig-mark-on-light',
    'hull-mark-on-dark', 'hull-mark-on-light', 'brig-lockup-on-dark',
    'brig-lockup-on-light', 'brig-lockup-badge', 'hull-lockup-on-dark',
    'hull-lockup-on-light']}

PALETTE = [
    ('Navy', '#0E2233', 'Field, and the ink on light grounds'),
    ('Deep', '#071521', 'Porthole glass'),
    ('Paper', '#F2EFE6', 'Ring and wordmark on dark'),
    ('Brass', '#E7A33E', 'Bars and water, on dark'),
    ('Brass deep', '#B9761C', 'Bars and water, on light'),
]

FILES = [
    ('brig-avatar.svg / .png', 'Org and repo avatar', 'brig-sh/brig'),
    ('brig-mark-on-dark.svg', 'Mark alone, dark grounds', 'all four repos'),
    ('brig-mark-on-light.svg', 'Mark alone, light grounds', 'all four repos'),
    ('brig-lockup-on-dark.svg', 'README header, dark theme', 'brig-sh/brig'),
    ('brig-lockup-on-light.svg', 'README header, light theme', 'brig-sh/brig'),
    ('brig-lockup-badge.svg', 'Slides, uncontrolled grounds', 'brig-sh/brig'),
    ('hull-*.svg / .png', 'The same set for hull', 'brig-sh/hull'),
]

sizes = ''.join(
    f'<figure class="sz"><img class="tile" src="{S["brig-avatar"]}" alt="brig avatar at {n}px" '
    f'width="{n}" height="{n}"><figcaption>{n}px</figcaption></figure>'
    for n in (128, 48, 24, 16))

pal = ''.join(
    f'<div class="sw"><span class="chip" style="background:{hexv}"></span>'
    f'<div><b>{nm}</b><code>{hexv}</code><p>{use}</p></div></div>'
    for nm, hexv, use in PALETTE)

rows = ''.join(
    f'<tr><td><code>{f}</code></td><td>{d}</td><td>{w}</td></tr>'
    for f, d, w in FILES)

HTML = f'''<title>brig / hull identity</title>
<style>
  :root {{
    --navy:#0E2233; --deep:#071521; --paper:#F2EFE6; --brass:#E7A33E;
    --brass-deep:#B9761C; --slate:#8B9BA9; --line:rgba(242,239,230,.14);
    --sans:"Avenir Next","Avenir",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    --serif:Georgia,"Iowan Old Style","Times New Roman",serif;
    --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--navy); color:var(--paper);
    font-family:var(--serif); font-size:17px; line-height:1.65;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap {{ max-width:880px; margin:0 auto; padding:0 28px 96px; }}
  h1,h2,h3,.eyebrow,figcaption,th,.chip+div b {{ font-family:var(--sans); }}
  h1 {{ font-size:34px; font-weight:600; letter-spacing:-.02em; margin:0;
       text-wrap:balance; }}
  h2 {{ font-size:15px; font-weight:600; letter-spacing:.16em;
       text-transform:uppercase; color:var(--brass); margin:0; }}
  .eyebrow {{ font-family:var(--mono); font-size:12px; letter-spacing:.18em;
             text-transform:uppercase; color:var(--slate); margin:0; }}
  p {{ margin:0; max-width:64ch; }}
  section {{ display:flex; flex-direction:column; gap:18px; padding:52px 0;
            border-top:1px solid var(--line); }}
  /* the rivet motif, borrowed from the mark, as the only ornament */
  section::before {{
    content:""; display:block; height:5px; width:100%;
    background-image:radial-gradient(circle, var(--brass) 2.5px, transparent 2.6px);
    background-size:34px 5px; background-repeat:repeat-x; opacity:.5;
    margin-top:-53px; margin-bottom:22px;
  }}
  header {{ display:flex; flex-direction:column; align-items:center; gap:26px;
           text-align:center; padding:88px 0 64px; }}
  header img {{ width:132px; height:132px; border-radius:22px;
               box-shadow:0 0 0 1px var(--line), 0 18px 44px rgba(0,0,0,.45); }}
  .lede {{ font-size:20px; line-height:1.55; color:var(--paper); }}
  .grid2 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
           gap:20px; }}
  .card {{ border:1px solid var(--line); border-radius:14px; padding:26px;
          display:flex; flex-direction:column; align-items:center; gap:16px;
          background:var(--deep); }}
  .card img {{ width:120px; height:120px; }}
  .card b {{ font-family:var(--mono); font-size:13px; letter-spacing:.1em;
            text-transform:uppercase; color:var(--brass); }}
  .card p {{ font-size:15px; color:var(--slate); text-align:center; }}
  .sizes {{ display:flex; align-items:flex-end; gap:34px; flex-wrap:wrap;
           padding:26px; border:1px solid var(--line); border-radius:14px; }}
  .tile {{ border-radius:14%; box-shadow:0 0 0 1px var(--line); }}
  .sz {{ margin:0; display:flex; flex-direction:column; align-items:center; gap:10px; }}
  figcaption {{ font-family:var(--mono); font-size:11px; color:var(--slate);
               letter-spacing:.1em; }}
  .ground {{ border-radius:14px; padding:34px; display:flex; justify-content:center;
            align-items:center; gap:30px; flex-wrap:wrap; }}
  .ground.light {{ background:#fff; }}
  .ground.dark {{ background:#0d1117; border:1px solid var(--line); }}
  .ground img {{ max-width:100%; height:56px; }}
  .sw {{ display:flex; gap:16px; align-items:flex-start; }}
  .chip {{ width:46px; height:46px; border-radius:10px; flex:none;
          border:1px solid var(--line); }}
  .sw code {{ font-family:var(--mono); font-size:12px; color:var(--brass);
             margin-left:10px; }}
  .sw p {{ font-size:14px; color:var(--slate); }}
  .tw {{ overflow-x:auto; }}
  table {{ border-collapse:collapse; width:100%; font-size:14px; min-width:520px; }}
  th,td {{ text-align:left; padding:11px 14px; border-bottom:1px solid var(--line);
          vertical-align:top; }}
  th {{ font-size:11px; letter-spacing:.14em; text-transform:uppercase;
       color:var(--slate); font-weight:600; }}
  td code {{ font-family:var(--mono); font-size:12.5px; color:var(--paper); }}
  .rules {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
           gap:14px; list-style:none; padding:0; margin:0; }}
  .rules li {{ border-left:2px solid var(--brass); padding:4px 0 4px 16px;
              font-size:15px; color:var(--slate); }}
  .todo {{ border:1px solid var(--brass); border-radius:14px; padding:26px;
          background:rgba(231,163,62,.07); display:flex; flex-direction:column; gap:12px; }}
  .todo code {{ font-family:var(--mono); font-size:13px; color:var(--brass); }}
  a {{ color:var(--brass); }}
  a:focus-visible, img:focus-visible {{ outline:2px solid var(--brass); outline-offset:3px; }}
  @media (max-width:560px) {{ h1 {{ font-size:27px; }} header {{ padding:56px 0 40px; }} }}
</style>

<div class="wrap">
  <header>
    <img src="{S['brig-avatar']}" alt="The brig avatar: a barred porthole">
    <div>
      <p class="eyebrow">brig-sh &middot; visual identity</p>
      <h1>A porthole, and what you put behind it</h1>
    </div>
    <p class="lede">The mark is a porthole. <b>brig</b> bars it, because a brig
    is the cell aboard a ship. <b>hull</b> leaves it open on water, because the
    hull is the vessel the sandbox is carved out of.</p>
  </header>

  <section>
    <h2>One silhouette, two contents</h2>
    <p>The two projects share a shape rather than a wordmark. That is the whole
    system: anything else in the org gets the same porthole with something else
    behind the glass.</p>
    <div class="grid2">
      <div class="card">
        <img src="{S['brig-mark-on-dark']}" alt="brig mark">
        <b>brig</b>
        <p>Bars across the glass. The agent gets a window on the world and no
        way through it.</p>
      </div>
      <div class="card">
        <img src="{S['hull-mark-on-dark']}" alt="hull mark">
        <b>hull</b>
        <p>Open water. The runtime the sandbox is cut from, not the cell
        itself.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>Legibility</h2>
    <p>GitHub shows an org avatar at 16&ndash;20px in commit lists and around
    48px in listings. These are those sizes, not a scaled mockup.</p>
    <div class="sizes">{sizes}</div>
    <p>The rivets stop resolving at about 24px. That is intended: they are
    texture, not information, and the ring plus three bars carries the mark
    down to 16px.</p>
  </section>

  <section>
    <h2>Lockups on both grounds</h2>
    <p>The README header sits behind a <code>&lt;picture&gt;</code>, so it
    follows the reader's theme. These are the two files that swap.</p>
    <div class="ground light">
      <img src="{S['brig-lockup-on-light']}" alt="brig lockup, light">
      <img src="{S['hull-lockup-on-light']}" alt="hull lockup, light">
    </div>
    <div class="ground dark">
      <img src="{S['brig-lockup-on-dark']}" alt="brig lockup, dark">
      <img src="{S['hull-lockup-on-dark']}" alt="hull lockup, dark">
    </div>
  </section>

  <section>
    <h2>Palette</h2>
    <p>Brass because ships are brass. Navy because it is the sea, and because
    it keeps us off the cloud-native blue everything else uses.</p>
    <div class="grid2">{pal}</div>
  </section>

  <section>
    <h2>Files</h2>
    <div class="tw"><table>
      <thead><tr><th>File</th><th>Use</th><th>Lives in</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p>The wordmark is Avenir Next Demi Bold converted to outlines, so no file
    here depends on a font being installed.</p>
  </section>

  <section>
    <h2>Rules</h2>
    <ul class="rules">
      <li>Never put the on-dark mark on a light ground. The ring is paper
      coloured and disappears.</li>
      <li>Keep clear space of one ring width around the mark.</li>
      <li>Do not re-colour the bars. Brass on navy is the pairing that survives
      both GitHub themes.</li>
      <li>The avatar ships with no baked corner radius. GitHub rounds it.</li>
    </ul>
  </section>

  <section>
    <h2>The one manual step</h2>
    <div class="todo">
      <p>The org avatar cannot be set over the API --
      <code>avatar_url</code> is read-only on the org endpoint, and the
      Packages-style REST surface does not cover it either. It is a web-UI
      upload.</p>
      <p><b>github.com/organizations/brig-sh/settings/profile</b> &rarr; upload
      <code>~/develop/brig-artwork/png/brig-avatar-512.png</code></p>
    </div>
  </section>
</div>
'''

with open(OUT, 'w') as f:
    f.write(HTML)
print('wrote', OUT, os.path.getsize(OUT) // 1024, 'KB')
