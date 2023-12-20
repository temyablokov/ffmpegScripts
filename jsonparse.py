import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def parse_json_metrics(file):

    with open(file, 'r') as file:
        content = file.read()

    vmaf_dict = {
        "integer_adm2": [],
        "integer_adm_scale0": [],
        "integer_adm_scale1": [],
        "integer_adm_scale2": [],
        "integer_adm_scale3": [],
        "integer_motion2": [],
        "integer_motion": [],
        "integer_vif_scale0": [],
        "integer_vif_scale1": [],
        "integer_vif_scale2": [],
        "integer_vif_scale3": [],
        "vmaf": [],
        "n": []
    }

    psnr_dict = {
                "n": [],
                "mse_avg": [],
                "mse_y": [],
                "mse_u": [],
                "mse_v": [],
                "psnr_avg": [],
                "psnr_y": [],
                "psnr_u": [],
                "psnr_v": []
            }

    ssim_dict = {
                "n": [],
                "ssim_y": [],
                "ssim_u": [],
                "ssim_v": [],
                "ssim_avg": []
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

def plot_metrics(metrics_data_list, codec_names, metric_name):
    metrics_keys = list(metrics_data_list[0].keys())
    metrics_keys.remove('n')

    rows = len(metrics_keys)
    cols = 1

    fig = make_subplots(rows=rows, cols=cols, shared_xaxes=True,
                        subplot_titles=[f'{submetric} comparison for codecs' for submetric in metrics_keys],
                        vertical_spacing=0.01,
                        horizontal_spacing=0.05
                        )

    for i, submetric in enumerate(metrics_keys, start=1):
        for metrics_data, codec_name in zip(metrics_data_list, codec_names):
            fig.add_trace(go.Scatter(x=metrics_data['n'], y=metrics_data[submetric], mode='lines', 
                                     name=codec_name, line=dict(width=0.9)),
                          row=i, col=1)

    fig.update_xaxes(title_text='Frame', row=rows, col=1)
    fig.update_yaxes(title_text=metric_name, col=1)

    fig.update_layout(
        autosize=False,
        height=10000,
        width = 2000,  
        showlegend=True,
         margin=dict(l=0, r=0, t=0, b=0),
        # xaxis=dict(
        #     rangeslider=dict(visible=True),
        #     type="linear"
        # ),
        font=dict(
            size=10,
            color='#000000'
        )
    )

    fig.show()

metrics_h264 = "D:\SystemFolders\Videos\BBBunny\output_h264_vs_output_metrics.txt"
metrics_h265 = "D:\SystemFolders\Videos\BBBunny\output_h265_vs_output_metrics.txt"
metrics_vp9 = "D:\SystemFolders\Videos\BBBunny\output_vp9_vs_output_metrics.txt"
metrics_av1 = "D:\SystemFolders\Videos\BBBunny\output_av1_vs_output_metrics.txt"

h264_vmaf, h264_psnr, h264_ssim = parse_json_metrics(metrics_h264)
h265_vmaf, h265_psnr, h265_ssim = parse_json_metrics(metrics_h265)
vp9_vmaf, vp9_psnr, vp9_ssim = parse_json_metrics(metrics_vp9)
av1_vmaf, av1_psnr, av1_ssim = parse_json_metrics(metrics_av1)



vmaf_data_list = [h264_vmaf, h265_vmaf, vp9_vmaf, av1_vmaf]
psnr_data_list = [h264_psnr, h265_psnr, vp9_psnr, av1_psnr]
ssim_data_list = [h264_ssim, h265_ssim, vp9_ssim, av1_ssim]
codec_names = ['H264', 'H265', 'VP9', 'AV1']

plot_metrics(vmaf_data_list, codec_names, "VMAF")
plot_metrics(ssim_data_list, codec_names, "SSIM")
plot_metrics(psnr_data_list, codec_names, "PSNR")