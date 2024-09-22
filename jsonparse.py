import json
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import re
import os

def parse_json_metrics(file):
    with open(file, 'r') as file:
        content = json.load(file)

    vmaf_df = pd.json_normalize(content['vmaf'])
    psnr_df = pd.json_normalize(content['psnr'])
    ssim_df = pd.json_normalize(content['ssim'])

    return vmaf_df, psnr_df, ssim_df

def extract_name(filename):
    pattern = r'(\w+)_lib((\w+[-\w]+)_(\d+)M)_vs_(\w+)_metrics\.txt'
    match = re.match(pattern, filename)
    if match:
        codec = match.group(2)
        bitrate = f"{match.group(3)}M"
        return codec, bitrate
    return None, None

def add_metrics_to_df(df, new_data, codec, bitrate):
    new_data['codec'] = codec
    new_data['bitrate'] = bitrate
    if df is None:
        return new_data
    else:
        return pd.concat([df, new_data], ignore_index=True)

def plot_metrics(df, metrics_to_plot, metric_name):
    fig = make_subplots(rows=1, cols=1, subplot_titles=(metrics_to_plot[metric_name],))
    for bitrate in df['bitrate'].unique():
        bitrate_df = df[df['bitrate'] == bitrate]
        for column in bitrate_df.columns:
            if column not in ['n', 'codec', 'bitrate']:
                for codec in bitrate_df['codec'].unique():
                    codec_df = bitrate_df[bitrate_df['codec'] == codec]
                    x_values = codec_df['n'] if 'n' in codec_df.columns else list(range(1, len(codec_df) + 1))
                    y_values = codec_df[column]
                    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name=f"{codec} - {column}"), row=1, col=1)

    fig.update_layout(title=f"{metrics_to_plot[metric_name]}")
    fig.show()

def plot_metrics_from_files(dir, metrics_to_plot):
    metrics = {
        'vmaf': 'VMAF Metrics',
        'psnr': 'PSNR Metrics',
        'ssim': 'SSIM Metrics'
    }

    vmaf_df = None
    psnr_df = None
    ssim_df = None

    for filename in os.listdir(dir):
        if filename.endswith('metrics.txt'):
            codec, bitrate = extract_name(filename)
            if codec:
                vmaf_data, psnr_data, ssim_data = parse_json_metrics(os.path.join(dir, filename))
                vmaf_df = add_metrics_to_df(vmaf_df, vmaf_data, codec, bitrate)
                psnr_df = add_metrics_to_df(psnr_df, psnr_data, codec, bitrate)
                ssim_df = add_metrics_to_df(ssim_df, ssim_data, codec, bitrate)

    if 'vmaf' in metrics_to_plot:
        plot_metrics(vmaf_df, metrics, 'vmaf')
    if 'psnr' in metrics_to_plot:
        plot_metrics(psnr_df, metrics, 'psnr')
    if 'ssim' in metrics_to_plot:
        plot_metrics(ssim_df, metrics, 'ssim')

# Uncomment the following line to run the function
# plot_metrics_from_files("D:\\SystemFolders\\Videos\\video_samples", ['vmaf', 'psnr'])