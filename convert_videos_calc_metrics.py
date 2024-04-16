import os.path
import subprocess
import ffmpeg

def encode_yuv(yuv_file, bitrates):
    base_name = os.path.splitext(yuv_file)[0]

    codecs = ['libx264', 'libx265', 'libvpx-vp9', 'libsvtav1']
    extensions = ['mp4', 'mp4', 'webm', 'mp4']

    outputs = []

    for bitrate in bitrates:
        for codec, ext in zip(codecs, extensions):
            output_name = f"{base_name}_{codec}_{bitrate}M.{ext}"

            ffmpeg.input(
                yuv_file, format='rawvideo', pix_fmt='yuv420p', s='1920x1080'#, r=30
            ).output(output_name, vcodec=codec, b=f'{bitrate}M', t=5, r=30).run()

            outputs.append(output_name)

    return outputs

def calculate_metrics(ref, dist, metrics_list):
    command = ['ffmpeg-quality-metrics', dist, ref, '-m'] + metrics_list
    try:
        ref_name = os.path.basename(ref).split('.')[0]
        dist_name = os.path.basename(dist).split('.')[0]
        print(f"started {dist_name} vs {ref_name}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout

        ref_name = os.path.basename(ref).split('.')[0]
        dist_name = os.path.basename(dist).split('.')[0]

        output_file_name = f"{dist_name}_vs_{ref_name}_metrics.txt"
        output_file_path = os.path.join(os.path.dirname(dist), output_file_name)

        with open(output_file_path, 'w') as output_file:
            output_file.write(output)
        print(f'Results written in {output_file_name}')

    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")
        print(f"Вывод ошибки: {e.output}")

# Путь к файлу с видео
yuv_name = "D:\\SystemFolders\\Videos\\video_samples\\WITCHER3.y4m"

# Список битрейтов
bitrates = [2, 5]

encoded_files = encode_yuv(yuv_name, bitrates)

metrics = ['psnr', 'ssim', 'vmaf']

for encoded_file in encoded_files:
    calculate_metrics(yuv_name, encoded_file, metrics)
