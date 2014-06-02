---
title: Color-coding experiments
layout: default
---

Turktools encourages setting a unique **"code"** for each experiment generated, so that Workers can avoid participating in the same experiment multiple times. In the template skeletons provided with turktools, this code is simply printed and presented to the user, with the text "Please complete at most one {% raw %}{{code}}{% endraw %} survey. You will not be paid for completing more than one survey with this code." However, it has been suggested that a more effective method would be to have experiments vary in a **border color**. This variation is easy to implement in your template skeletons.

## Step 1: add the border color code

Add the following code to your template skeleton:

	<style type="text/css">
	body {
		border: 10px black solid;
		border-color: {% raw %}{{code}}{% endraw %};
		margin: 0px;
		padding: 10px;
	}
	</style>

This CSS code creates a very visible 10 pixel border around the experiment. When the `templater` generates an HTML template from this skeleton, it will replace the ``{% raw %}{{code}}{% endraw %}`` [substitution tag](https://github.com/mitcho/turktools/wiki/Substitution-tags) with the color code.

## Step 2: modify code text to refer to the border color

Modify the skeleton's text referring to the `{% raw %}{{code}}` to now refer to this colored border instead. In the bundled skeletons, there are two references to `{{code}}{% endraw %}`. The one at the top could be replaced by:

    <p class="red" style="text-transform: uppercase"><strong>Please complete at most one <span class="blue">{% raw %}{{code}}{% endraw %}</span> border survey. You will not be paid for completing more than one survey with this color.</strong></p>

The one at the bottom of the survey could be replaced by:

    <h3 style="color: red; text-align:center;">After submitting this HIT, do NOT submit another HIT with a <span class="blue">{% raw %}{{code}}{% endraw %}</span> border. You will not be paid for completing more than one survey with this color.</h3>

## Step 3: when creating an experiment, choose an appropriate color code

When using this setup, the experiment code that you use must be a known CSS color code. Here are 17 standard ones:

aqua, black, blue, fuchsia, gray, grey, green, lime, maroon, navy, olive, purple, red, silver, teal, white, and yellow