import os
import subprocess
import ffmpeg

def encode_yuv(yuv_file, bitrates, resolutions, frame_rates):
    base_name = os.path.splitext(yuv_file)[0]

    codecs = ['libx264', 'libx265', 'libvpx-vp9', 'libsvtav1']
    extensions = ['mp4', 'mp4', 'webm', 'mp4']

    outputs = []

    for bitrate in bitrates:
        for resolution in resolutions:
            for frame_rate in frame_rates:
                for codec, ext in zip(codecs, extensions):
                    output_name = f"{base_name}_{codec}_{bitrate}M_{resolution}_{frame_rate}fps.{ext}"
                    
                    width, height = map(int, resolution.split('x'))
                    
                    ffmpeg.input(
                        yuv_file, format='rawvideo', pix_fmt='yuv420p', s=resolution, r=frame_rate
                    ).output(
                        output_name, vcodec=codec, b=f'{bitrate}M', t=5, r=frame_rate
                    ).run()
                    
                    outputs.append(output_name)
    
    return outputs

def calculate_metrics(ref, dist, metrics_list):
    command = ['ffmpeg-quality-metrics', dist, ref, '-m'] + metrics_list
    try:
        ref_name = os.path.basename(ref).split('.')[0]
        dist_name = os.path.basename(dist).split('.')[0]
        print(f"Started calculating metrics for {dist_name} vs {ref_name}")
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout

        output_file_name = f"{dist_name}_vs_{ref_name}_metrics.txt"
        output_file_path = os.path.join(os.path.dirname(dist), output_file_name)

        with open(output_file_path, 'w') as output_file:
            output_file.write(output)
        
        print(f'Results written in {output_file_name}')
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Error output: {e.output}")

def main():
    witcher_path = "D:\\SystemFolders\\Videos\\video_samples\\Witcher\\WITCHER3.y4m"
    csgo_path = "D:\\SystemFolders\\Videos\\video_samples\\CSGO\\CSGO.y4m"
    dota_path = "D:\\SystemFolders\\Videos\\video_samples\\DOTA2\\DOTA2.y4m"

    bitrates = [2, 5, 7]
    resolutions = ['1280x720', '1920x1080', '3840x2160']
    frame_rates = [30]
    metrics = ['psnr', 'ssim', 'vmaf']

    yuv_name =  dota_path  

  
    encoded_files = encode_yuv(yuv_name, bitrates, resolutions, frame_rates)

    for encoded_file in encoded_files:
        calculate_metrics(yuv_name, encoded_file, metrics)

if __name__ == "__main__":
    main()
