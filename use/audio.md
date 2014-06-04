---
title: Using audio playback
layout: default
---

For many experimental designs, it is useful or necessary to have participants listen to an audio recording. Turktools includes a sample audio playback skeleton, `binary-audio.skeleton.html`. This page discusses technical details relevant to preparing and serving audio files with this and similar templates.

## Audio playback with HTML5 Audio

Modern browsers include built-in support for audio playback using the new `<audio>` HTML tag. This allows for audio playback on websites without the use of JavaScript or a plugin such as Flash. The sample skeleton `binary-audio.skeleton.html` uses this `<audio>` tag.

Unfortunately, not all browsers support the same set of audio file formats for use with `<audio>`. Most modern browsers support the common mp3 format, but Firefox's support for mp3 is currently dependent on the operating system and environment. Firefox (as well as some other browsers) instead supports and encourages the use of the [ogg vorbis file format](https://en.wikipedia.org/wiki/Vorbis) (`.ogg`). See more information on [supported audio file formats](https://developer.mozilla.org/en-US/docs/Web/HTML/Supported_media_formats).

This means that for your experiment to run seamlessly across the vast majority of Workers, it may be necessary to encode all of your audio stimuli in both of these audio formats. If you choose to use only mp3 sources, some users may run into issues with your stimuli, in the form of missing audio controls or audio controls which cannot play, and may report having a poor experience with your experiment. Note, however, that the proportion of browsers which cannot play back mp3 format is decreasing over time. 

The `<audio>` tag allows for multiple source files of different formats to be specified for a single audio clip. The following example HTML code, used in `binary-audio.skeleton.html` for the first practice item, shows how this is specified:

	<audio controls="controls" preload="auto">
		Your browser does not support the <code>audio</code> element. You cannot participate in this HIT.
		<source src="http://turktools.net/images/test1.mp3" type="audio/mp3">
		<source src="http://turktools.net/images/test1.ogg" type="audio/ogg">
	</audio>

We'll take a look at this `<audio>` code piece by piece. The `<audio>` tag first wraps around a bit of default text which is displayed in browsers which do not recognize the `<audio>` tag (Internet Explorer prior to 2011 and other browsers prior to 2008). The `<audio>` tag then uses two `<source>` tags to specify two different audio files---the same audio, one in mp3 format and one in ogg format---with corresponding information on the audio encodings used. The `<audio>` tag itself has two properties: `controls` so that the browser's UI for controlling audio playback is displayed, and `preload` set to encourage the browser to pre-download the audio files prior to the user-initiated playback. See [more information](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio) on the `<audio>` tag.

The sample code in this skeleton can easily be modified to different experimental tasks. For example, each item block could be modified to include:

* two audio clips to be compared
* an audio clip and a corresponding image
* an audio clip and corresponding text

For each of these modifications, the template skeleton will require additional "fields," and items in the raw items file will have to have the corresponding data in the correct order. Read more about [substitution tags](/use/tags.html).

## Additional JavaScript code in the skeleton

The `binary-audio.skeleton.html` template includes an additional bit of JavaScript code which makes it so that the "natural"/"unnatural" buttons cannot be pressed until the corresponding audio clip has reached the end. (Technically, this is triggered by the HTML5 Audio API's `ended` event.) This helps to ensure that users with JavaScript enabled cannot answer an item before they have listened to the audio.

With the script as written in `binary-audio.skeleton.html`, users without JavaScript enabled will simply not have this feature enabled, but will still be able to play the audio and participate in the experiement. It may be advantageous instead to strictly require JavaScript to be enabled, for example by using CSS to hide the experimental items by default and using JavaScript, if enabled, to unhide the items.

## Final notes

Hosting experiments with audio stimuli brings its own technical challenges. We strongly suggest using the Simulator to test each individual survey, as it will be presented to participants, on multiple modern browsers, to make sure that the audio loads and behaves as expected.

Finally, we note that it is also possible to use video playback in experiments using the HTML5 `<video>` tag, which follows a syntax very similar to that of the `<audio>` tag described here. Just as we discussed with the `<audio>` tag above, though, browser support for different video encoding formats differ. Here is [an overview of supported file formats](https://developer.mozilla.org/en-US/docs/Web/HTML/Supported_media_formats).
