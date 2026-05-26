const fs = require('fs');
const path = require('path');

const files = ["index.html", "profil.html", "kolaborasi.html", "alumni.html", "pmb.html", "portal.html"];
const mapping = {
    "Profil": "profil.html",
    "Aktifitas": "kolaborasi.html",
    "Ekstra": "kolaborasi.html",
    "Kolaborasi": "kolaborasi.html",
    "PMB": "pmb.html",
    "Beranda": "index.html",
    "Karya": "alumni.html",
    "Alumni": "alumni.html"
};

const mobileScript = `
<script>
document.addEventListener('DOMContentLoaded', function() {
    let menuBtn = document.querySelector('button:has(.material-symbols-outlined[data-icon="menu"]), button:has(span:contains("menu"))');
    // Fallback if the first selector fails
    if (!menuBtn) {
        const spans = Array.from(document.querySelectorAll('span.material-symbols-outlined'));
        const targetSpan = spans.find(span => span.textContent.trim() === 'menu');
        if (targetSpan) {
            menuBtn = targetSpan.closest('button');
        }
    }
    
    if (menuBtn) {
        // Create a mobile menu container if it doesn't exist
        let mobileMenu = document.createElement('div');
        mobileMenu.className = 'fixed inset-0 bg-white/95 dark:bg-emerald-950/95 z-[100] hidden flex-col items-center justify-center space-y-8';
        mobileMenu.innerHTML = \`
            <a href="index.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Beranda</a>
            <a href="profil.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Profil</a>
            <a href="kolaborasi.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Kolaborasi & Aktifitas</a>
            <a href="alumni.html" class="text-2xl font-noto-serif text-emerald-900 dark:text-emerald-50">Karya & Alumni</a>
            <a href="pmb.html" class="text-2xl font-noto-serif text-amber-600 font-bold">PMB</a>
            <button class="absolute top-6 right-6 text-emerald-900 dark:text-emerald-50 close-menu">
                <span class="material-symbols-outlined" style="font-size: 32px">close</span>
            </button>
        \`;
        document.body.appendChild(mobileMenu);

        menuBtn.addEventListener('click', () => {
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
`;

files.forEach(fname => {
    const filePath = path.join(__dirname, fname);
    if (!fs.existsSync(filePath)) {
        console.log(\`File not found: \${fname}\`);
        return;
    }

    let content = fs.readFileSync(filePath, 'utf8');

    // Replace links
    for (const [text, url] of Object.entries(mapping)) {
        // Regex to match <a ... href="...">...Text...</a>
        // It's a bit tricky in JS regex, but we can just use a simple string replacement for the exact text if we know the structure
        // Let's use a function replacer
        const regex = new RegExp(\`(<a[^>]*?href=["'])([^"']*)(["'][^>]*?>\\\\s*\` + text + \`\\\\s*</a>)\`, 'gi');
        content = content.replace(regex, \`$1\` + url + \`$3\`);
    }

    // Wrap logo
    if (content.includes('alt="IDDC Logo"')) {
        content = content.replace(/(<div[^>]*?>\s*)(<img[^>]*?alt=["']IDDC Logo["'][^>]*?>)(\s*<\/div>)/gi, '$1<a href="index.html">$2</a>$3');
    }

    // Insert mobile script
    if (content.includes('</body>') && !content.includes('mobileMenu.classList.add')) {
        content = content.replace('</body>', mobileScript);
    }

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(\`Processed: \${fname}\`);
});

console.log('All done.');
