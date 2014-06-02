---
title: Checking for previous participants
layout: default
---

Turktools encourages setting a unique "code" for each experiment generated, so that Workers can avoid participating in the same experiment multiple times. However, this requires the Worker to pay attention to this code. An alternative is to add JavaScript code to your template which will automatically check the Worker's ID against a list of known, previous WorkerIDs, and block the Worker from participating in the same experiment multiple times.

There are two ways to implement this kind of Worker ID check feature:

1. **Checking against a database of IDs on a server:** An external server keeps track of the list of Workers, which will be continually updated as new Workers participate in your experiment. However, this requires running your own server to keep this database, or the use of a third-party service for this purpose such as Myle Ott's [Unique Turker](http://uniqueturker.myleott.com/).
2. **Checking against a static list of IDs:** A fixed list of previous Worker IDs is included with your experiment's template. The advantage of this approach is that the checking code is completely contained in the template, with no requirement for an external server. The disadvantage is that this list must be manually maintained and is only updated when new batches are uploaded. This means that repeat participants from previous related experiments can be detected, but multiple submissions from a single Worker against a single batch cannot be blocked. This static list can also be used to block Workers who are known to be problematic.

In the remainder of this page, we give sample code for checking Worker IDs against a static list of IDs (method 2 above).

## Sample checking code

The following code can be added to your template or template skeleton:

	<script type="text/javascript">
	// set the list of previous participant WorkerIDs here:
	// (WorkerIDs can be separated by spaces, commas, and even line breaks)
	var previous = 'ATHGVB5K1EOZW A20KZBL2PA6ZW';
	
	var message = "You have already completed this survey. Please go back by clicking 'Return HIT.'";

	var match = /workerId=(.*?)&/.exec(window.location);
	var previousArray = previous.split(/[,\s]+/);
	if ( match.length == 2 && previousArray.indexOf(match[1]) != -1 ) {
		// the current worker is in the list of previous workers
		document.getElementById('mturk_form').style.display = 'none';
		document.getElementsByTagName('body')[0].innerHTML = message;
	}
	</script>
	<p><input type="text" /></p>

The list of previous participants' WorkerIDs go in the variable `previous`, at the top of the code snippet above. The message which will be displayed to Workers who are in the list of known participants can be modified in the variable `message`.
