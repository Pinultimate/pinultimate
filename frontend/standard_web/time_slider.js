/* Requires JQuery UI */

var createTimeSlider = function(divID,changeFunction,slideFunction) {

  var me = this; // Disambiguates scope

  me.timerInterval = null;
  me.MAX_VALUE = 23;
  me.MIN_VALUE = 0;
  me.STEP_VALUE = 1;
  me.TIMER_MILLI_SECONDS = 1000;

  var parentDiv = $("#"+divID);

  // Create time label
  var timeLabel = $(document.createElement("p")).text("0:00");
  timeLabel.css( {
    "margin-bottom":5,
    "text-align": "center"
  });
  // Create slider
	var slider = $(document.createElement("div")).slider({
      min: this.MIN_VALUE,
      max: this.MAX_VALUE,
      step: this.STEP_VALUE,
      // Change is called when the slider is released and value was changed
      change: function(event, ui) {
        timeLabel.text(slider.slider("value") + ":00");
        if (changeFunction) {
          changeFunction();
        }
      },
      // Slider is called whenever the slider value is changed
      slide: function(event, ui) {
        timeLabel.text(slider.slider("value") + ":00");
        if (slideFunction) {
          slideFunction();
        }
      }
  });
  slider.width(parentDiv.width()*2/3);
  slider.css("float","right");

  var playButton = $(document.createElement("div")).text("play")
  playButton.click(function() {
    console.log("Clicked!");
    if (me.timerInterval) {
      // Pause
      clearInterval(me.timerInterval);
      me.timerInterval = null;
    } else {
      //Start Timer
      me.timerInterval = setInterval(function() {
        console.log("timer set");
        var value = slider.slider("value");
        if (value >= MAX_VALUE) {
          clearInterval(me.timerInterval);
        }
        slider.slider("value",value+1);
      },me.TIMER_MILLI_SECONDS);
    }
  });

  playButton.css("float","left");

  parentDiv.append(timeLabel);
  parentDiv.append(playButton);
  parentDiv.append(slider);
  // This final div just allows the last two divs to be floated
  parentDiv.append($(document.createElement("div")).css("clear","both"));
}