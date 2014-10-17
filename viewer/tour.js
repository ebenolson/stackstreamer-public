// Instance the tour
var tour = new Tour({
  steps: [
  {
    element: false,
    title: "Navigation",
    content: "<ul><li>Left-click and drag to pan</li><li>Use the scroll wheel to zoom in and out</li><li>Hold CTRL or left-click and scroll to change layers</li></ul>"
  },
  {
    element: "#layericon0",
    title: "Layer indicator",
    placement:"left",
    content: "The current layer is shown in red. Click a layer to navigate there."
  },
  {
    element: "#helpbutton",
    title: "Help",
    placement:"left",
    content: "Click this button to show this tour of the viewer functions."
  },
  {
    element: "#backbutton",
    title: "Go Back",
    placement:"left",
    content: "Click here to exit viewer and return to the stack organizer."
  },
  {
    element: "#homebutton",
    title: "Home",
    placement:"left",
    content: "Zoom out completely and center the stack in the viewport."
  },
  {
    element: "#flagbutton",
    title: "Flags",
    placement:"left",
    content: "Open the flag panel. Create flags to quickly return to areas of interest."
  },
  {
    element: "#arrowbutton",
    title: "Arrow Marker",
    placement:"left",
    content: "Open the arrow panel to view and place markers."
  },
  {
    element: "#snapshotbutton",
    title: "Snapshot",
    placement:"left",
    content: "Download an image of the current view"
  },
  {
    element: "#exportbutton",
    title: "Export Data",
    placement:"left",
    content: "Select a region of data to download"
  },
  {
    element: "#hideinfobutton",
    title: "Fullscreen",
    placement:"left",
    content: "Hide all overlays. Press ESC to exit fullscreen mode."
  },

],
debug:true,
storage:false,
orphan:true,
});

// Initialize the tour
tour.init();

function doTour() {
  tour.restart();
}