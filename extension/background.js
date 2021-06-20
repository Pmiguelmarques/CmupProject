const socket = new WebSocket('ws://localhost:8080');

socket.addEventListener('message', function(event){
    console.log(event.data);
})

socket.addEventListener('open', function(event){
    
    socket.send('Connected');

    chrome.tabs.onActivated.addListener(tab => {
        chrome.tabs.get(tab.tabId, current_tab_info => {
            socket.send(current_tab_info.url);
        })

    })

    chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){
        socket.send(tab.url);
    })
})
