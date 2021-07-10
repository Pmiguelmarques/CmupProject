"use strict";

var not_allowed_urls = [];

function initialize_socket(not_allowed_urls) {
  var socket = new WebSocket('ws://localhost:8080');
  socket.addEventListener('message', function (event) {
    console.log("new blacklist page " + event.data);

    if (not_allowed_urls.indexOf(event.data) > -1) {} else {
      not_allowed_urls.push(String(event.data));
    }

    for (var i = 0; i < not_allowed_urls.length; i++) {
      console.log("Array NAU -> " + not_allowed_urls[i]);
    }
  });
  socket.addEventListener('open', function (event) {
    socket.send('Connected');
    chrome.tabs.onActivated.addListener(function (tab) {
      //console.log(tab.url); -> undefined
      setTimeout(function () {
        getCurrentTab(tab, socket, not_allowed_urls);
      }, 500);
    });
    chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
      console.log("Updated on onUpdated");
      socket.send(tab.url); //socket.send(tab.title);

      if (not_allowed_urls.indexOf(String(tab.url)) > -1) {
        console.log("This page is distracting"); //alert("This page is distracting");
      }
    });
  });
  socket.addEventListener('close', function (event) {
    setTimeout(function () {
      initialize_socket(not_allowed_urls);
    }, 60);
  });
}

initialize_socket(not_allowed_urls);

function getCurrentTab(tab, socket, not_allowed_urls) {
  chrome.tabs.get(tab.tabId, function (current_tab_info) {
    //socket.send("Updated on onActivated");
    console.log("current tab " + current_tab_info.url);
    socket.send(current_tab_info.url); //socket.send(current_tab_info.title);

    if (not_allowed_urls.indexOf(String(current_tab_info.url)) > -1) {
      console.log("This page is distracting"); //alert("This page is distracting");
    }
  });
}

function getNewRequest(request) {
  if (request && request.url) {
    if (request.type == "main_frame" || request.type == "sub_frame") {
      for (var i = 0; i < not_allowed_urls.length; i++) {
        console.log("Array NAU -> " + not_allowed_urls[i]);

        if (request.url.indexOf(not_allowed_urls[i]) > -1) {
          URLStorage = request.url;
          return {
            redirectUrl: chrome.extension.getURL("blocked_page.html")
          };
        }
      }
    }
  }
}

chrome.webRequest.onBeforeRequest.addListener(getNewRequest, {
  urls: ["*://*/*"]
}, ['blocking']);