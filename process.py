import os
import re

files = ["index.html", "profil.html", "kolaborasi.html", "alumni.html", "pmb.html", "portal.html"]
mapping = {
    "Profil": "profil.html",
    "Aktifitas": "kolaborasi.html",
    "Ekstra": "kolaborasi.html",
    "Kolaborasi": "kolaborasi.html",
    "PMB": "pmb.html",
    "Beranda": "index.html",
    "Karya": "alumni.html",
    "Alumni": "alumni.html"
}

mobile_script = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.querySelector('button:has(.material-symbols-outlined[data-icon="menu"]), button:has(span:contains("menu"))');
    // Fallback if the first selector fails depending on how icon is inserted
    let actualMenuBtn = menuBtn;
    if (!actualMenuBtn) {
        const spans = document.querySelectorAll('span.material-symbols-outlined');
        for (const span of spans) {
            if (span.textContent.trim() === 'menu') {
                actualMenuBtn = span.closest('button');
                break;
            }
        }
    }
    
    if (actualMenuBtn) {
        // Create a mobile menu container if it doesn't exist
        let mobileMenu = document.createElement('div');
        mobileMenu.className = 'fixed inset-0 bg-white/95 dark:bg-emerald-950/95 z-[100] hidden flex-col items-center justify-center space-y-8';
        mobileMenu.innerHTML = `
            <a href="index.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Beranda</a>
            <a href="profil.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Profil</a>
            <a href="kolaborasi.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Kolaborasi & Aktifitas</a>
            <a href="alumni.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Karya & Alumni</a>
            <a href="pmb.html" class="text-2xl font-noto-serif text-amber-600 font-bold">PMB</a>
            <button class="absolute top-6 right-6 text-emerald-900 dark:text-emerald-50 close-menu">
                <span class="material-symbols-outlined" style="font-size: 32px">close</span>
            </button>
        `;
        document.body.appendChild(mobileMenu);

        actualMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.remove('hidden');
            mobileMenu.classList.add('flex');
        });
        
        mobileMenu.querySelector('.close-menu').addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            mobileMenu.classList.remove('flex');
        });
    }
});
</script>
</body>
"""

for fname in files:
    if not os.path.exists(fname):
        print(f"File not found: {fname}")
        continue
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace links
    for text, url in mapping.items():
        # Match <a ... href="...">Text</a>
        # Use regex to replace the href part
        pattern = r'(<a[^>]*?href=["\']).*?(["\'][^>]*?>\s*' + re.escape(text) + r'\s*</a>)'
        content = re.sub(pattern, r'\g<1>' + url + r'\g<2>', content)

    # Wrap logo with link to index.html if it's not already linked
    # Logo is typically an image with alt="IDDC Logo"
    logo_pattern = r'(<img[^>]*?alt=["\']IDDC Logo["\'][^>]*?>)'
    # check if logo is already inside an <a> tag
    # Simplified approach: just replace the logo img tag with a wrapped version if not already wrapped
    # Actually, let's just make the parent div of the logo clickable by replacing its HTML
    if "alt=\"IDDC Logo\"" in content and "<a href=\"index.html\"" not in content[:content.find("alt=\"IDDC Logo\"")]:
        content = re.sub(r'(<div[^>]*?>\s*)(<img[^>]*?alt=["\']IDDC Logo["\'][^>]*?>)(\s*</div>)', r'\1<a href="index.html">\2</a>\3', content)

    # Insert script before </body>
    if "</body>" in content and "<script>" not in content.split("</body>")[0][-1000:]: # rough check if script is already there
        content = content.replace("</body>", mobile_script)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)

print("Processing complete.")
