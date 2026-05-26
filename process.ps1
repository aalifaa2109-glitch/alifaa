$files = @("index.html", "profil.html", "kolaborasi.html", "alumni.html", "pmb.html", "portal.html")

$mapping = @{
    "Profil" = "profil.html"
    "Aktifitas" = "kolaborasi.html"
    "Ekstra" = "kolaborasi.html"
    "Kolaborasi" = "kolaborasi.html"
    "PMB" = "pmb.html"
    "Beranda" = "index.html"
    "Karya" = "alumni.html"
    "Alumni" = "alumni.html"
}

$mobileScript = @"
<script>
document.addEventListener('DOMContentLoaded', function() {
    let menuBtn = document.querySelector('button:has(.material-symbols-outlined[data-icon=`"menu`"]), button:has(span:contains(`"menu`"))');
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
"@

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content -Path $file -Raw -Encoding UTF8

        foreach ($key in $mapping.Keys) {
            $val = $mapping[$key]
            # Replace <a href="#">Key</a> with <a href="val">Key</a>
            $content = [regex]::Replace($content, '(<a[^>]*?href=["''])[^"'']*?(["''][^>]*?>\s*' + $key + '\s*</a>)', '$1' + $val + '$2', 'IgnoreCase')
        }

        # Wrap logo
        $content = [regex]::Replace($content, '(<div[^>]*?>\s*)(<img[^>]*?alt=["'']IDDC Logo["''][^>]*?>)(\s*</div>)', '$1<a href="index.html">$2</a>$3', 'IgnoreCase')

        # Insert mobile script
        if ($content -match '</body>' -and $content -notmatch 'mobileMenu\.classList\.add') {
            $content = $content.Replace('</body>', $mobileScript)
        }

        Set-Content -Path $file -Value $content -Encoding UTF8
        Write-Host "Processed: $file"
    } else {
        Write-Host "File not found: $file"
    }
}

Write-Host "All done."
