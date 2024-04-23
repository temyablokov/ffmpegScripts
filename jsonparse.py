import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import re
import os

def parse_json_metrics(file):

    with open(file, 'r') as file:
        content = file.read()

    vmaf_dict = {
        # "integer_adm2": [],
        # "integer_adm_scale0": [],
        # "integer_adm_scale1": [],
        # "integer_adm_scale2": [],
        # "integer_adm_scale3": [],
        # "integer_motion2": [],
        # "integer_motion": [],
        # "integer_vif_scale0": [],
        # "integer_vif_scale1": [],
        # "integer_vif_scale2": [],
        # "integer_vif_scale3": [],
        "vmaf": [],
        "n": []
    }

    psnr_dict = {
                "n": [],
                # "mse_avg": [],
                # "mse_y": [],
                # "mse_u": [],
                # "mse_v": [],
                "psnr_avg": []
                # "psnr_y": [],
                # "psnr_u": [],
                # "psnr_v": []
            }

    ssim_dict = {
                # "n": [],
                # "ssim_y": [],
                # "ssim_u": [],
                # "ssim_v": [],
                # "ssim_avg": []
            }

    vmaf_keys = vmaf_dict.keys()
    ssim_keys = ssim_dict.keys()
    psnr_keys = psnr_dict.keys()

    data = json.loads(content)

    for item in data['vmaf']:
        for key in vmaf_keys:
            vmaf_dict[key].append(item[key])

    for item in data['psnr']:
        for key in psnr_keys:
            psnr_dict[key].append(item[key])

    for item in data['ssim']:
        for key in ssim_keys:
            ssim_dict[key].append(item[key])

    return vmaf_dict, psnr_dict, ssim_dict

def extract_name(filename):
    pattern = r'(\w+)_lib((\w+[-\w]+)_(\d+)M)_vs_(\w+)_metrics\.txt'
    match = re.match(pattern, filename)
    if match:
        codec = match.group(2)
        bitrate = f"{match.group(3)}M"
        return codec, bitrate
    return None, None

def plot_metrics_from_files(dir, metrics_to_plot):
    metrics = {
        'vmaf': 'VMAF Metrics',
        'psnr': 'PSNR Metrics',
        'ssim': 'SSIM Metrics'
    }

    metric_dict = {
        'vmaf': {},
        'psnr': {},
        'ssim': {}
    }

    for filename in os.listdir(dir):
        if filename.endswith('metrics.txt'):
            codec, bitrate = extract_name(filename)
            if codec:
                vmaf_data, psnr_data, ssim_data = parse_json_metrics(os.path.join(dir, filename))

                for metric_name, metric_data in zip(['vmaf', 'psnr', 'ssim'], [vmaf_data, psnr_data, ssim_data]):
                    if metric_name in metrics_to_plot:
                        if bitrate not in metric_dict[metric_name]:
                            metric_dict[metric_name][bitrate] = {}
                        for key, values in metric_data.items():
                            if key == 'n': 
                                continue

                            if 'n' in metric_data: 
                                x_values = metric_data['n']
                            else:
                                x_values = list(range(1, len(values) + 1))  

                            if key not in metric_dict[metric_name][bitrate]:
                                metric_dict[metric_name][bitrate][key] = []
                            metric_dict[metric_name][bitrate][key].append(
                                go.Scatter(x=x_values, y=values, mode='lines', name=f"{codec} - {key}")
                            )
    
    print("dict len: ", len(metric_dict))

    for metric_name, traces in metric_dict.items():
        if metric_name in metrics_to_plot:
            for bitrate, traces_data in traces.items():
                fig = make_subplots(rows=1, cols=1, subplot_titles=(metrics[metric_name],))
                for key, trace_set in traces_data.items(): 
                    for t in trace_set:
                        fig.add_trace(t, row=1, col=1)

                fig.update_layout(title=f"{metrics[metric_name]} at {bitrate}")
                fig.show()

plot_metrics_from_files("D:\\SystemFolders\\Videos\\video_samples", ['vmaf', 'psnr'])


