# virtus
Virtus is a anti-AI CAPTCHA system, using a technique that creates videos where shapes are invisible to AI vision systems but clearly visible to human observers. It exploits fundamental differences between human and artificial visual processing.

How It Works

The Core Principle: Temporal Coherence

The human visual system is extraordinarily sensitive to temporal coherence - patterns that remain stable over time while surrounding elements change. This is a survival mechanism that helps us detect predators, track moving objects, and perceive structure in complex environments.
AI vision systems, by contrast, analyze each frame independently and look for spatial statistical patterns. They cannot easily detect temporal coherence without being specifically trained for it.
The Algorithm

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



Why It Works
Human Vision Advantages:

Evolved to detect subtle motion and temporal patterns
Integrates information across multiple frames
Excellent at figure-ground segregation
Can perceive "sameness" even in random patterns

AI Vision Limitations:

Trained on spatial patterns, not temporal coherence
Each frame analyzed independently in most systems
No inherent mechanism for detecting "stability" in noise
Statistical properties of both regions are identical

Implementation Details
Key Parameters

Block Size: Not critical in simple version, used in image quilting variants
Noise Type: Pure random RGB values (0-255 per channel)
Mask Shape: Any binary mask (circle, text, custom shape)
Frame Rate: 30 fps recommended for video

The JavaScript Version (Original)
The original code you shared uses "image quilting" - a more sophisticated texture synthesis method:

Takes patches from a source texture
Stitches them with minimal seam visibility
Creates more natural-looking noise patterns
Uses masks to preserve specific regions between passes

The Python Version (Simplified)
Our implementation uses a simpler approach:

Direct random noise generation
Binary masking for temporal preservation
Produces statistically uniform noise
Easier to understand and modify

Applications
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

Advantages Over Traditional CAPTCHAs

AI-Resistant: Exploits fundamental perceptual gap
Scalable: Easy to generate unlimited variations
Accessible: Can be described in audio for vision-impaired users
Fast: Humans can identify patterns quickly
Difficult to Train Against: Would require massive temporal datasets

Limitations

Still Images Less Effective: Works best with animation where temporal coherence is obvious
Display Requirements: Needs consistent frame timing
May Not Work on All Displays: Very low-quality screens might blur effects
Novel Attack Vector: Eventually AI could be trained on temporal patterns

Future Improvements

Use subtle motion within the masked region (drift, flow)
Combine with other perceptual phenomena (apparent motion, etc.)
Multi-layer temporal coherence (nested patterns)
Adaptive difficulty based on user performance

Scientific Basis
This technique is inspired by research on:

Visual motion perception
Figure-ground segregation
Temporal integration in visual cortex
Differences between biological and artificial vision systems

The original research you referenced (PRX Life 2.023004) likely explores similar perceptual phenomena at the intersection of physics and neuroscience.
Usage
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

Conclusion
This technique demonstrates a genuine perceptual gap between human and AI vision that is economically impractical to close through training. It represents a practical application of neuroscience research to create truly AI-resistant verification systems.
