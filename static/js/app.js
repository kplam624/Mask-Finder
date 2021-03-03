// This javascript file is only if we need to use it.
// Not sure of the purpose yet.

// Experimental code to save and image to session storage.

var yesButton = d3.select("button").attr("class","yes");

yesButton.on("click", runClick);

function runClick(){
    d3.json("/webcamcapture", function(data){
        var result = data;

        console.log(result);
    })
};
