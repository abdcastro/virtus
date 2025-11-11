# virtus

Virtus is a anti-AI CAPTCHA system, using a technique that creates videos where shapes are invisible to AI vision systems but clearly visible to human observers. It exploits fundamental differences between human and artificial visual processing.

In this repository, we offer the core noise generation code that makes this effect possible.

Astraea AI will soon offer the full integration of this system to your business on request.

Reach out to https://www.linkedin.com/in/abdcastro/ for any questions.

----------------------------------------------------------------------------------------

How It Works:

The human visual system is extraordinarily sensitive to temporal coherence - patterns that remain stable over time while surrounding elements change. This is a survival mechanism that helps us detect predators, track moving objects, and perceive structure in complex environments.
AI vision systems, by contrast, analyze each frame independently and look for spatial statistical patterns. They cannot easily detect temporal coherence without being specifically trained for it.

Generate Base Noise: Create a frame filled with random pixel values (pure visual noise)
Define a Mask: Create a shape (circle, letter, etc.) that defines which pixels should remain stable
Two-Pass Synthesis:

First Pass: Generate complete random noise for the entire image
Second Pass: Regenerate ALL pixels with NEW random noise, EXCEPT pixels within the masked shape


Result:

The masked area keeps its original noise pattern (temporal coherence)
Everything else is regenerated (temporal incoherence)
To AI: Looks like uniform random noise (statistically identical)
To humans: The shape "pops out" due to temporal stability

Why It Works:

Human Vvsion evolved to detect subtle motion and temporal patterns
Integrates information across multiple frames
Excellent at figure-ground segregation
Can perceive "sameness" even in random patterns

AI is trained on spatial patterns, not temporal coherence
Each frame analyzed independently in most systems
No inherent mechanism for detecting "stability" in noise
Statistical properties of both regions are identical

Implementation Details:

Block Size: Not critical in simple version, used in image quilting variants
Noise Type: Pure random RGB values (0-255 per channel)
Mask Shape: Any binary mask (circle, text, custom shape)
Frame Rate: 30 fps recommended for video

Applications:

1. AI-Resistant CAPTCHAs

Show animated noise with hidden letters/numbers
Humans easily read them
AI cannot detect patterns
Economically impractical to train AI on this

2. Watermarking

Hide authentication patterns in video/images
Invisible to AI content analysis
Verifiable by humans

3. Security Challenges

Prove human presence without traditional puzzles
No accessibility issues (audio can describe what to look for)
Cannot be solved by current AI models

4. Research Tool

Study differences in human vs AI perception
Test visual processing mechanisms
Develop new computer vision approaches

Scientific Basis:

This technique is inspired by research on:

Visual motion perception
Figure-ground segregation
Temporal integration in visual cortex
Differences between biological and artificial vision systems

Usage:

Generate Static Image:
bashpython3 hidden_shape_generator.py
Generate Animated GIF:
bashpython3 hidden_shape_generator.py video
Customize:
Edit the script to modify:

Image dimensions
Circle size and path
Number of frames
Animation speed
