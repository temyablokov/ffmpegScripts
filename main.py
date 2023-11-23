import os.path
import subprocess
import ffmpeg


def encode_yuv(yuv_file):
    base_name = os.path.splitext(yuv_file)[0]

    output_h264 = base_name + "_h264.mp4"
    output_h265 = base_name + "_h265.mp4"
    output_vp9 = base_name + "_vp9.webm"
    output_av1 = base_name + "_av1.mp4"

    ffmpeg.input(
        yuv_file, format='rawvideo', pix_fmt='yuv420p', s='1920x1080'
    ).output(output_h264, vcodec='libx264').run()
    ffmpeg.input(
        yuv_file, format='rawvideo', pix_fmt='yuv420p', s='1920x1080'
    ).output(output_h265, vcodec='libx265').run()
    ffmpeg.input(
        yuv_file, format='rawvideo', pix_fmt='yuv420p', s='1920x1080'
    ).output(output_vp9, vcodec='libvpx-vp9').run()
    ffmpeg.input(
        yuv_file, format='rawvideo', pix_fmt='yuv420p', s='1920x1080'
    ).output(output_av1, vcodec='libsvtav1').run()

    return output_h264, output_h265, output_vp9, output_av1



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


metrics = ['psnr', 'ssim', 'vmaf']
yuv_name = "D:\Videos\BBBunny\output.y4m"
h264 = "D:\Videos\BBBunny\output_h264.mp4"
h265 = "D:\Videos\BBBunny\output_h265.mp4"
vp9 = "D:\Videos\BBBunny\output_vp9.webm"
av1 = "D:\Videos\BBBunny\output_av1.mp4"

calculate_metrics(yuv_name, h264, metrics)
calculate_metrics(yuv_name, h265, metrics)
calculate_metrics(yuv_name, vp9, metrics)
calculate_metrics(yuv_name, av1, metrics)