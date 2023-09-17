function injectIconStyles(csspath) {
    const link_icon = document.createElement('link');
    link_icon.rel = 'stylesheet';
    link_icon.type = 'text/css';
    link_icon.href = chrome.runtime.getURL(csspath); // Make sure the CSS file path is correct

    document.head.appendChild(link_icon);

}

// Call the function to inject the styles when needed
injectIconStyles('icon.css');

injectIconStyles('window.css');



// Create a div element for the floating icon
const icon = document.createElement('div');
icon.className = 'edu-thank-you-icon';
icon.textContent = '👍';

// Apply styles to the icon
icon.style.position = 'fixed';
icon.style.top = '50%';
icon.style.right = '10px';
icon.style.transform = 'translateY(-50%)';
icon.style.backgroundColor = 'white';
icon.style.color = 'black';
icon.style.fontSize = '20px';
icon.style.border = '1px solid #ccc';
icon.style.borderRadius = '50%';
icon.style.width = '40px';
icon.style.height = '40px';
icon.style.textAlign = 'center';
icon.style.lineHeight = '40px';
icon.style.zIndex = '9999';
icon.style.cursor = 'pointer';

let expanded = false; // Track whether the window is expanded

let whiteWindow = document.createElement('div');

let current_url = "";
// Create a function to toggle the window's visibility
function toggleWindow() {
    if (!expanded) {
        expanded = true;
        showWhiteWindow();
    } else {
        expanded = false;
        hideWhiteWindow();
    }
}

chrome.runtime.sendMessage({type: 'getCurrentTabURL'}, function(response) {
    if (response.url) {
        console.log('Current tab URL is:', response.url);
        current_url = response.url;
        // You can now use the URL for whatever you wish
    } else {
        console.error('Failed to fetch the current tab URL.');
    }
});



// Function to create and show the white window
function showWhiteWindow() {
    chrome.runtime.sendMessage({type: 'getCurrentTabURL'}, function(response) {
        if (response.url) {
            console.log('Current tab URL is:', response.url);
            current_url = response.url;
            // You can now use the URL for whatever you wish
        } else {
            console.error('Failed to fetch the current tab URL.');
        }
    });

    whiteWindow = document.createElement('div');
    whiteWindow.className = 'edu-thank-you-window';
    whiteWindow.textContent = 'WIGO';

    // Apply styles to the white window
    whiteWindow.style.position = 'fixed';
    whiteWindow.style.top = '50%';
    whiteWindow.style.right = '10px';
    whiteWindow.style.transform = 'translateY(-50%)';
    whiteWindow.style.backgroundColor = 'white';
    whiteWindow.style.color = 'black';
    whiteWindow.style.fontSize = '16px';
    whiteWindow.style.border = '1px solid #ccc';
    whiteWindow.style.padding = '10px';
    whiteWindow.style.borderRadius = '5px';
    whiteWindow.style.zIndex = '9999';
    whiteWindow.style.width = '0';
    whiteWindow.style.overflow = 'hidden';
    whiteWindow.style.transition = 'width 0.3s';

    document.body.appendChild(whiteWindow);


    // Create a return icon
    const returnIcon = document.createElement('div');
    returnIcon.className = 'edu-thank-you-return';
    returnIcon.textContent = '↩️'; // Unicode arrow icon for "return"
    returnIcon.style.position = 'absolute';
    returnIcon.style.top = '10px';
    returnIcon.style.right = '10px';
    returnIcon.style.fontSize = '20px';
    returnIcon.style.cursor = 'pointer';

    // Add a click event listener to the return icon
    returnIcon.addEventListener('click', hideWhiteWindow);



    // Create three buttons with hyperlinks
    const button1 = document.createElement('a');
    button1.className = 'white-window-button';

    button1.textContent = 'Analyze Website!';
    button1.href = 'http://localhost:8050/data?url='+document.URL;
    button1.style.display = 'block';
    button1.style.margin = '10px 0';
    button1.style.padding = '10px';
    button1.style.textAlign = 'center';
    button1.style.backgroundColor = '#007bff';
    button1.style.color = 'white';
    button1.style.textDecoration = 'none';
    button1.style.border = 'none';
    button1.style.borderRadius = '5px';
    button1.style.cursor = 'pointer';
    //
    // const button2 = document.createElement('a');
    // button2.className = 'white-window-button';
    // button2.textContent = 'Visit Site 2';
    // button2.href = 'https://www.example.com/site2?url='+document.URL;
    //
    // const button3 = document.createElement('a');
    // button3.className = 'white-window-button';
    // button3.textContent = 'Visit Site 3';
    // button3.href = 'https://www.example.com/site3';

    // Add buttons to the window
    whiteWindow.appendChild(returnIcon);
    whiteWindow.appendChild(button1);
    // whiteWindow.appendChild(button2);
    // whiteWindow.appendChild(button3);



    // Expand the white window
    setTimeout(() => {
        whiteWindow.style.width = '200px';
    }, 10);

}

// Function to hide the white window
function hideWhiteWindow() {
    const returnIcon = document.querySelector('.edu-thank-you-return');
    if (returnIcon) {
        returnIcon.remove();
    }
    const whiteWindow = document.querySelector('.edu-thank-you-window');
    if (whiteWindow) {
        whiteWindow.remove();
    }
}

// Add a click event listener to the icon
icon.addEventListener('click', toggleWindow);

// Add the icon to the page
document.body.appendChild(icon);

