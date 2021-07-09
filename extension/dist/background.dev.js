"use strict";

function initialize_socket() {
  var socket = new WebSocket('ws://localhost:8080');
  socket.addEventListener('message', function (event) {
    console.log(event.data);
  });
  socket.addEventListener('open', function (event) {
    socket.send('Connected');
    chrome.tabs.onActivated.addListener(function (tab) {
      //console.log(tab.url); -> undefined
      setTimeout(function () {
        getCurrentTab(tab, socket);
      }, 100);
    });
    chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
      console.log("Updated on onUpdated");
      socket.send(tab.url);
      socket.send(tab.title);
    });
  });
  socket.addEventListener('close', function (event) {
    setTimeout(function () {
      initialize_socket();
    }, 60);
  });
}

initialize_socket();

function getCurrentTab(tab, socket) {
  chrome.tabs.get(tab.tabId, function (current_tab_info) {
    socket.send("Updated on onActivated");
    console.log("current tab " + current_tab_info.url);
    socket.send(current_tab_info.url);
    socket.send(current_tab_info.title);
  });
}