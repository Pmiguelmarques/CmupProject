const socket = new WebSocket('ws://localhost:8080');



socket.addEventListener('open', function(event){
    
    socket.send('Connected');

    chrome.tabs.onActivated.addListener(tab => {
        chrome.tabs.get(tab.tabId, current_tab_info => {
            socket.send(current_tab_info.url);
        })
    })
})
