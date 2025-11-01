"""
CAPTCHA Challenge Generator - Hidden Shapes in Noise
Creates videos where shapes move in noise, visible to humans but not AI
"""

import numpy as np
from PIL import Image, ImageDraw
import random
import json


def generate_noise_texture(width, height):
    """Generate a random noise texture"""
    noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return noise


def create_circle_mask(width, height, center_x, center_y, radius):
    """Create a circular mask"""
    mask = np.zeros((height, width), dtype=np.uint8)
    y, x = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    mask[dist_from_center <= radius] = 1
    return mask


def create_square_mask(width, height, center_x, center_y, size):
    """Create a square mask"""
    mask = np.zeros((height, width), dtype=np.uint8)
    half_size = size // 2
    
    x_start = max(0, center_x - half_size)
    x_end = min(width, center_x + half_size)
    y_start = max(0, center_y - half_size)
    y_end = min(height, center_y + half_size)
    
    mask[y_start:y_end, x_start:x_end] = 1
    return mask


def generate_frame_with_mask(width, height, mask, previous_frame=None):
    """
    Generate a frame where the masked area is temporally coherent
    """
    # Generate completely new random noise
    output = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # If we have a previous frame, copy the masked region from it
    if previous_frame is not None:
        mask_3d = np.stack([mask, mask, mask], axis=2)
        output = np.where(mask_3d, previous_frame, output)
    
    return output


def create_captcha_video(output_path, shape='circle', direction='clockwise', 
                        width=640, height=480, num_frames=60, shape_size=80):
    """
    Create a CAPTCHA video with hidden shape moving in specified direction
    
    Args:
        output_path: Path to save the GIF
        shape: 'circle' or 'square'
        direction: 'clockwise' or 'counterclockwise'
        width, height: Video dimensions
        num_frames: Number of frames
        shape_size: Size of the hidden shape (radius for circle, side length for square)
    """
    frames = []
    
    # Center of circular path
    center_x = width // 2
    center_y = height // 2
    path_radius = min(width, height) // 3
    
    # Generate initial frame
    base_frame = None
    
    for frame_idx in range(num_frames):
        print(f"Generating frame {frame_idx + 1}/{num_frames}")
        
        # Calculate position on circular path
        if direction == 'clockwise':
            angle = (frame_idx / num_frames) * 2 * np.pi
        else:  # counterclockwise
            angle = -(frame_idx / num_frames) * 2 * np.pi
        
        pos_x = int(center_x + path_radius * np.cos(angle))
        pos_y = int(center_y + path_radius * np.sin(angle))
        
        # Create mask for current position
        if shape == 'circle':
            mask = create_circle_mask(width, height, pos_x, pos_y, shape_size)
        else:  # square
            mask = create_square_mask(width, height, pos_x, pos_y, shape_size)
        
        # Generate frame
        frame = generate_frame_with_mask(width, height, mask, base_frame)
        
        # Store this frame as base for next iteration
        if base_frame is None:
            base_frame = frame.copy()
        
        frames.append(Image.fromarray(frame))
    
    # Save as GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,  # 20 fps
        loop=0
    )
    
    print(f"CAPTCHA video saved to {output_path}")
    return {
        'shape': shape,
        'direction': direction,
        'frames': num_frames,
        'size': shape_size
    }


def generate_challenge(output_dir, challenge_id=None):
    """
    Generate a random CAPTCHA challenge
    Returns the challenge metadata
    """
    if challenge_id is None:
        challenge_id = random.randint(1000, 9999)
    
    # Randomly select shape and direction
    shape = random.choice(['circle', 'square'])
    direction = random.choice(['clockwise', 'counterclockwise'])
    
    output_path = f"{output_dir}/challenge_{challenge_id}.gif"
    
    print(f"\nGenerating challenge {challenge_id}")
    print(f"Shape: {shape}, Direction: {direction}")
    
    metadata = create_captcha_video(
        output_path=output_path,
        shape=shape,
        direction=direction,
        width=640,
        height=480,
        num_frames=60,
        shape_size=80
    )
    
    metadata['id'] = challenge_id
    metadata['filename'] = f"challenge_{challenge_id}.gif"
    
    # Save metadata
    with open(f"{output_dir}/challenge_{challenge_id}.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "generate":
            # Generate a random challenge
            metadata = generate_challenge("/mnt/user-data/outputs")
            print(f"\nChallenge generated!")
            print(f"Answer: {metadata['shape']} moving {metadata['direction']}")
        
        elif sys.argv[1] == "test":
            # Generate all 4 variants for testing
            output_dir = "/mnt/user-data/outputs"
            
            variants = [
                ('circle', 'clockwise'),
                ('circle', 'counterclockwise'),
                ('square', 'clockwise'),
                ('square', 'counterclockwise')
            ]
            
            for shape, direction in variants:
                filename = f"test_{shape}_{direction}.gif"
                print(f"\n{'='*50}")
                print(f"Generating: {shape} - {direction}")
                print(f"{'='*50}")
                
                create_captcha_video(
                    output_path=f"{output_dir}/{filename}",
                    shape=shape,
                    direction=direction,
                    width=640,
                    height=480,
                    num_frames=60,
                    shape_size=80
                )
    else:
        print("Usage:")
        print("  python captcha_generator.py generate  - Generate a random challenge")
        print("  python captcha_generator.py test      - Generate all 4 variants")
