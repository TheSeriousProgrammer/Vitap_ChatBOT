var botui = new BotUI('my-botui-app');

var response = null;

var last_request = "";

var url = "http://localhost:8080/?query=";
//var url = "https://vitapchatbot.duckdns.org/?query=";

function feedback() {
    bot_message("Was the results satisfactory?");
    botui.action.button({
        action: [{
            "text": "Good Response👍",
            "value": "👍"
        }, {
            "text": "Bad Response👎",
            value: "👎"
        }]
    }).then(function(res) {
        bot_message("Thank you for your feedback");
        if (res.value == "👎") {
            var http = new XMLHttpRequest();
            http.timeout = 1500;
            http.open("GET", url + window.last_request.trim().replace(' ', '+') + "&mode=1", true)
            http.send(null);
        }

    });
}

function sleep(delay) {
    delay = 300;
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
    console.log("ok");

}


function initiateBotQuery() {
    bot_message("Here are a few sample queries");
    sleep(600);
    bot_message("Try Clicking one of queries below 👇");
    var samp_queries = ["who is pankaj", "how can i contact ellison", "what are the btech courses available", "what are the international collabrations"]
    var buttons = []
    for (var i = 0; i < samp_queries.length; i++) {
        buttons.push({
            "text": samp_queries[i],
            "value": samp_queries[i]
        })
        console.log(buttons);
    }

    botui.action.button({
        action: buttons
    }).then(function(res) {
        console.log("Value :" + res);
        bot_http_call(res.value, 1);
    });

}

function titleCase(str) {
    str = str.replace("(", " ( ");
    str = str.replace(")", " ) ");
    var splitStr = str.split(' ');
    for (var i = 0; i < splitStr.length; i++) {
        splitStr[i] = (splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1));
    }
    // Directly return the joined string
    var str2 = splitStr.join(' ');

    var splitStr1 = str2.split('-');
    for (var i = 0; i < splitStr1.length; i++) {
        splitStr1[i] = splitStr1[i].charAt(0).toUpperCase() + splitStr1[i].substring(1);
    }

    return splitStr1.join('-');
}

function processURLButtons(elements, mode) {
    /*This is to make sure that the buttons are refreshed
    even after using clicking a button to visit the webpage, but we wont the introductory "here are some links message for refreshes
    so a fresh call shoould pass some mode value to make sure that it is not undefined, inorder to make srue that the introdcution message "Here are some links" to be displayed */

    if (mode === undefined) {
        bot_message("Here are some links which can help you");
        sleep(600);
        bot_message("Click one of the below links 👇")
    }
    botui.action.button({
        action: elements
    }).then(function(res) {
        console.log("Link :" + res.value);
        speechOutput("Opening link in new tab");
        processURLButtons(elements, 1);
        if (!(window.open(res.value, "_blank"))) {
            alert("Please Allow Pop-UPs for better experience");
        }

    });
}


function speechOutput(inp_str, voice) {
    //Creating default parameter values..
    if (typeof voice === undefined) {
        voice = 'en-IN'
    }

    var msg = new SpeechSynthesisUtterance();
    msg.volume = 0.8;
    msg.rate = 1;
    msg.pitch = 0.78;
    msg.text = inp_str;
    msg.lang = voice;
    //sleep(300);
    window.speechSynthesis.speak(msg);
}

function bot_http_call(inp_str, mode) {
    console.log("Http Call Activated");
    if (mode == 0) { //0 for bot mode http mode , anything else for normal bot message
        return "You told " + inp_str;
    } else if (mode == 1) {
        var http = new XMLHttpRequest();
        //Kindly Bare with me , i usually dont write such big continuous chunk of code, if the language had been compiler based, the code wouldnt be shitty like this
        botui.message.add({
            loading:true
        }).then(function (index){

            http.onreadystatechange = function() {
                if (http.readyState == 4 && http.status == 200) { //Checks if the http call is made successfully
                    botui.message.remove(index);
                    console.log(http.responseText);
                    window.result = JSON.parse(http.responseText);
                    var inp_json = window.result;

                    if (inp_json["mode"] == 1) { //When mode == 1 the body just contains messages to be displayed to user
                        for (var i = 0; i < inp_json["body"].length; i++) {
                            bot_message(inp_json['body'][i]);
                            sleep(600);
                        }
                        feedback();
                    } else if (inp_json['mode'] == 0) { //When mode == 0, the results are from website search and is ["title","url"] format

                        var buttons = [];
                        for (var i = 0; i < inp_json["body"].length; i++) {
                            buttons.push({
                                "text": titleCase(inp_json['body'][i][0]),
                                "value": inp_json['body'][i][1]
                            });
                        }

                        processURLButtons(buttons);
                    } else if (inp_json['mode'] == 2) {
                        bot_message("Multiple Possiblities detected");
                        sleep(300);
                        bot_message("Click the appropriate choice 👇");
                        botui.action.button({
                            action: inp_json['body']
                        }).then(function(res) {
                            bot_http_call(res.value, 1);
                            console.log(res.value);
                        });

                    } else {
                        bot_message("Sorry Couldnt find information regarding the same");
                        sleep(800);
                        bot_message("I have noted down this issue");
                        bot_message("Try asking something else");
                        //initiateBotQuery();
                    }
                }
            }
        //http.timeout = 2500;
            http.onerror = function() {
                botui.message.remove(index);
                bot_message("Sorry for the inconvinience");
                sleep(600);
                bot_message("Check your internet connection , else server is down");
            }
            http.ontimeout = http.onerror;
            http.open("GET", url + inp_str.trim().replace(' ', '+') + "&mode=0", true)
            http.send(null);

        });
    
    } else {
        return inp_str;
    }

}


function key_boardinp() {
    botui.action.text({
        action: {
            placeholder: 'Type Here and press enter'
        }
    }).then(function(res) { // will be called when it is submitted.
        bot_http_call(res.value, 1);
        window.last_request = res.value.trim(); // will print whatever was typed in the field.

    });
}

function bot_message(inp_str) {
    var out_str = inp_str;
    window.botui.message.add({
        content: out_str,
     })
    speechOutput(out_str);
}

function user_message(inp_str) {
    window.botui.message.add({
        content: inp_str,
        human: true
    })
}

function callTheBot() {
    bot_message("Hello I am VITAP Chatbot, Here to assist you in this awesome Day");
    sleep(600);
    bot_message("Click the Keyboard icon below to type in your questions");
    sleep(600);
    bot_message("Would you like to see how i can help you?")
    sleep(600);
    botui.action.button({
        action: [{
            "text": "Yes!!",
            "value": "y"
        }, {
            "text": "May be Later 😔",
            "value": "n"
        }]
    }).then(function(res) {
        if (res.value == "y") {
            initiateBotQuery();
        }
    });

}
