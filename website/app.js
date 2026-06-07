// Mobile Navigation Toggle
const menuToggle = document.getElementById('menu-toggle');
const navMenu = document.getElementById('nav-menu');

menuToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    
    // Animate menu toggle icon (burger to X)
    const bars = menuToggle.querySelectorAll('.bar');
    bars[0].style.transform = navMenu.classList.contains('active') ? 'rotate(45deg) translate(5px, 6px)' : 'none';
    bars[1].style.opacity = navMenu.classList.contains('active') ? '0' : '1';
    bars[2].style.transform = navMenu.classList.contains('active') ? 'rotate(-45deg) translate(5px, -6px)' : 'none';
});

// Close menu when clicking a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const bars = menuToggle.querySelectorAll('.bar');
        bars[0].style.transform = 'none';
        bars[1].style.opacity = '1';
        bars[2].style.transform = 'none';
    });
});

// Accordion Control
document.querySelectorAll('.accordion-title').forEach(item => {
    item.addEventListener('click', () => {
        const parent = item.parentElement;
        const isActive = parent.classList.contains('active');
        
        // Close all accordion items
        document.querySelectorAll('.accordion-item').forEach(el => {
            el.classList.remove('active');
        });
        
        // Open clicked one if it wasn't active
        if (!isActive) {
            parent.classList.add('active');
        }
    });
});

// Console Tabs Control
function switchTab(tabId) {
    // Deactivate all tabs and hide all content
    document.querySelectorAll('.console-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Activate target
    const targetTab = Array.from(document.querySelectorAll('.console-tab')).find(tab => 
        tab.getAttribute('onclick').includes(tabId)
    );
    if (targetTab) targetTab.classList.add('active');
    
    const targetContent = document.getElementById(`tab-${tabId}`);
    if (targetContent) targetContent.classList.remove('hidden');
}

// Copy Console Commands
function copyConsole(btn) {
    const codeBlock = btn.parentElement.querySelector('code');
    if (!codeBlock) return;
    
    const text = codeBlock.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.background = '#10b981';
        btn.style.borderColor = '#10b981';
        btn.style.color = '#ffffff';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
            btn.style.borderColor = '';
            btn.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

// Live Pool Simulator (fluctuations to make page feel interactive and alive)
function startLiveSimulators() {
    const hashrateEl = document.getElementById('pool-hashrate');
    const minersEl = document.getElementById('pool-miners');
    
    let baseHashrate = 42.5; // MH/s
    let baseMiners = 12;
    
    setInterval(() => {
        // Random small change to hashrate (+/- 1.5 MH/s)
        const hashrateDelta = (Math.random() * 3 - 1.5);
        const currentHashrate = (baseHashrate + hashrateDelta).toFixed(2);
        hashrateEl.textContent = `${currentHashrate} MH/s`;
        
        // Random worker sign-on/sign-off (+/- 1 miner occasionally)
        if (Math.random() > 0.8) {
            const minerDelta = Math.random() > 0.5 ? 1 : -1;
            baseMiners = Math.max(5, baseMiners + minerDelta);
            minersEl.textContent = baseMiners;
        }
    }, 4000);
}

// Run on load
document.addEventListener('DOMContentLoaded', () => {
    startLiveSimulators();
});
