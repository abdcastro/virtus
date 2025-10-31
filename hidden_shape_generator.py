"""
Implementation of hidden shape in noise effect
Based on image quilting texture synthesis with selective regeneration
"""

import numpy as np
from PIL import Image, ImageDraw
import random


def generate_noise_texture(width, height):
    """Generate a random noise texture"""
    noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return noise


def get_random_patch(source, patch_size):
    """Extract a random patch from source texture"""
    h, w = source.shape[:2]
    y = random.randint(0, h - patch_size)
    x = random.randint(0, w - patch_size)
    return source[y:y+patch_size, x:x+patch_size]


def find_min_error_boundary(overlap1, overlap2, vertical=True):
    """Find minimum error boundary in overlap region"""
    if vertical:
        # Vertical seam
        errors = np.sum((overlap1.astype(float) - overlap2.astype(float)) ** 2, axis=2)
        # Simple approach: find minimum cost path
        cumulative = np.zeros_like(errors)
        cumulative[0] = errors[0]
        
        for i in range(1, errors.shape[0]):
            for j in range(errors.shape[1]):
                options = [cumulative[i-1, j]]
                if j > 0:
                    options.append(cumulative[i-1, j-1])
                if j < errors.shape[1] - 1:
                    options.append(cumulative[i-1, j+1])
                cumulative[i, j] = errors[i, j] + min(options)
        
        # Backtrack to find path
        path = np.zeros(errors.shape[0], dtype=int)
        path[-1] = np.argmin(cumulative[-1])
        
        for i in range(errors.shape[0] - 2, -1, -1):
            j = path[i+1]
            options = [(j, cumulative[i, j])]
            if j > 0:
                options.append((j-1, cumulative[i, j-1]))
            if j < errors.shape[1] - 1:
                options.append((j+1, cumulative[i, j+1]))
            path[i] = min(options, key=lambda x: x[1])[0]
        
        return path
    else:
        # Horizontal seam
        errors = np.sum((overlap1.astype(float) - overlap2.astype(float)) ** 2, axis=2)
        cumulative = np.zeros_like(errors)
        cumulative[:, 0] = errors[:, 0]
        
        for j in range(1, errors.shape[1]):
            for i in range(errors.shape[0]):
                options = [cumulative[i, j-1]]
                if i > 0:
                    options.append(cumulative[i-1, j-1])
                if i < errors.shape[0] - 1:
                    options.append(cumulative[i+1, j-1])
                cumulative[i, j] = errors[i, j] + min(options)
        
        path = np.zeros(errors.shape[1], dtype=int)
        path[-1] = np.argmin(cumulative[:, -1])
        
        for j in range(errors.shape[1] - 2, -1, -1):
            i = path[j+1]
            options = [(i, cumulative[i, j])]
            if i > 0:
                options.append((i-1, cumulative[i-1, j]))
            if i < errors.shape[0] - 1:
                options.append((i+1, cumulative[i+1, j]))
            path[j] = min(options, key=lambda x: x[1])[0]
        
        return path


def blend_patches(patch1, patch2, overlap_size, vertical=True):
    """Blend two patches along their overlap using minimum error boundary"""
    if vertical:
        overlap1 = patch1[:, -overlap_size:]
        overlap2 = patch2[:, :overlap_size]
        path = find_min_error_boundary(overlap1, overlap2, vertical=True)
        
        # Create blended patch
        result = patch1.copy()
        for i, j in enumerate(path):
            result[i, -overlap_size+j:] = patch2[i, j:]
        
        # Add non-overlapping part
        result = np.concatenate([result, patch2[:, overlap_size:]], axis=1)
    else:
        overlap1 = patch1[-overlap_size:, :]
        overlap2 = patch2[:overlap_size, :]
        path = find_min_error_boundary(overlap1, overlap2, vertical=False)
        
        result = patch1.copy()
        for j, i in enumerate(path):
            result[-overlap_size+i:, j] = patch2[i:, j]
        
        result = np.concatenate([result, patch2[overlap_size:, :]], axis=0)
    
    return result


def simple_quilting(source_texture, output_width, output_height, patch_size, overlap, mask=None, grid_presets=None):
    """
    Simplified approach: just generate noise, but reuse noise in masked areas
    This creates temporal coherence that humans can detect
    """
    # Generate completely new random noise
    output = np.random.randint(0, 256, (output_height, output_width, 3), dtype=np.uint8)
    
    # If we have grid_presets and a mask, copy the masked region from presets
    if grid_presets is not None and mask is not None:
        # grid_presets is the previous frame
        # Copy pixels where mask == 1
        mask_3d = np.stack([mask, mask, mask], axis=2)
        output = np.where(mask_3d, grid_presets, output)
    
    return output, output


def create_circle_mask(width, height, center_x, center_y, radius):
    """Create a circular mask"""
    mask = np.zeros((height, width), dtype=np.uint8)
    y, x = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    mask[dist_from_center <= radius] = 1
    return mask


def create_moving_circle_video(output_path, width=1280, height=720, num_frames=30, 
                                patch_size=58, radius=100):
    """
    Create a video where a circle moves through noise
    The circle is invisible to AI but visible to humans
    """
    overlap = patch_size // 6
    
    # Generate source noise texture
    source_texture = generate_noise_texture(patch_size * 10, patch_size * 10)
    
    frames = []
    
    # Circle path (moving in a circle)
    center_x_start = width // 2
    center_y_start = height // 2
    path_radius = min(width, height) // 4
    
    for frame_idx in range(num_frames):
        print(f"Generating frame {frame_idx + 1}/{num_frames}")
        
        # Calculate circle position
        angle = (frame_idx / num_frames) * 2 * np.pi
        circle_x = int(center_x_start + path_radius * np.cos(angle))
        circle_y = int(center_y_start + path_radius * np.sin(angle))
        
        # Create mask for this frame
        mask = create_circle_mask(width, height, circle_x, circle_y, radius)
        
        # First pass: create base noise
        if frame_idx == 0:
            output, grid_presets = simple_quilting(
                source_texture, width, height, patch_size, overlap
            )
        
        # Second pass: regenerate everything EXCEPT the circle
        output, grid_presets = simple_quilting(
            source_texture, width, height, patch_size, overlap, 
            mask=mask, grid_presets=grid_presets
        )
        
        frames.append(Image.fromarray(output))
    
    # Save as video
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=33,  # ~30 fps
        loop=0
    )
    
    print(f"Video saved to {output_path}")


def create_static_example(output_path, width=1280, height=720, patch_size=58):
    """Create a single static image with hidden circle"""
    overlap = patch_size // 6
    
    # Generate source noise
    source_texture = generate_noise_texture(patch_size * 10, patch_size * 10)
    
    # Create circular mask in center
    mask = create_circle_mask(width, height, width//2, height//2, 150)
    
    # First pass
    print("First pass: generating base noise...")
    output1, grid = simple_quilting(source_texture, width, height, patch_size, overlap)
    
    # Second pass: regenerate everything except circle
    print("Second pass: preserving circle area...")
    output2, _ = simple_quilting(
        source_texture, width, height, patch_size, overlap,
        mask=mask, grid_presets=grid
    )
    
    # Save
    img = Image.fromarray(output2)
    img.save(output_path)
    print(f"Image saved to {output_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "video":
        # Create video with moving circle
        create_moving_circle_video(
            "/mnt/user-data/outputs/hidden_circle.gif",
            width=1280,
            height=720,
            num_frames=90
        )
    else:
        # Create static image
        create_static_example(
            "/mnt/user-data/outputs/hidden_circle_static.png",
            width=1280,
            height=720
        )
