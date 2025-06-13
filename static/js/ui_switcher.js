document.addEventListener('DOMContentLoaded', function() {
    // Era switcher functionality
    const eraBtns = document.querySelectorAll('.era-btn');
    const currentEraDisplay = document.getElementById('current-era');
    
    // Set default era (2020s)
    let currentEra = '2020s';
    document.body.className = `era-${currentEra.toLowerCase()}`;
    currentEraDisplay.textContent = currentEra;
    
    eraBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const era = this.dataset.era;
            
            // Update active button
            eraBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Update body class and display
            document.body.className = `era-${era.toLowerCase()}`;
            currentEra = era;
            currentEraDisplay.textContent = era;
            
            // Update UI elements based on era
            updateUIForEra(era);
        });
    });
    
    function updateUIForEra(era) {
        const header = document.querySelector('header h1');
        
        switch (era) {
            case '1990s':
                header.innerHTML = '<marquee direction="right" scrollamount="3">MemeLord Chronos</marquee>';
                addUnderConstructionGif();
                break;
                
            case '2000s':
                header.innerHTML = 'Me<span style="color:#ff00ff">Me</span>Lord <span style="color:#33cc33">ChRoNoS</span> <span style="color:#ff9900">xD</span>';
                addGlitterText();
                break;
                
            case '2010s':
                header.textContent = 'MemeLord Chronos';
                addFilterEffect('sepia');
                break;
                
            case '2020s':
            default:
                header.textContent = 'MemeLord Chronos';
                removeEraEffects();
                break;
        }
    }
    
    function addUnderConstructionGif() {
        removeEraEffects();
        const constructionGif = document.createElement('div');
        constructionGif.className = 'era-effect under-construction';
        constructionGif.innerHTML = '<img src="/static/images/under_construction.gif" alt="Under Construction">';
        document.body.appendChild(constructionGif);
    }
    
    function addGlitterText() {
        removeEraEffects();
        const styleTag = document.createElement('style');
        styleTag.className = 'era-effect';
        styleTag.textContent = `
            .nav-link {
                background-image: url('/static/images/glitter.gif');
                background-size: cover;
                color: white;
                text-shadow: 2px 2px 5px black;
            }
        `;
        document.head.appendChild(styleTag);
    }
    
    function addFilterEffect(filter) {
        removeEraEffects();
        const styleTag = document.createElement('style');
        styleTag.className = 'era-effect';
        styleTag.textContent = `
            main {
                filter: ${filter}(0.7);
            }
        `;
        document.head.appendChild(styleTag);
    }
    
    function removeEraEffects() {
        document.querySelectorAll('.era-effect').forEach(el => el.remove());
    }
});
