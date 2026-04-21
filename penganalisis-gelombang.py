#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           :musical_score: PENGANALISIS GELOMBANG - Penukar Suara Kepada     ║
║                      Lukisan Visual                                          ║
║                                                                              ║
║           Nama Projek  : penganalisis-gelombang                              ║
║           Penulis    : misyaz-pelitari                                       ║
║           Keterangan : Skrip zurfanakan analisis audio dan mengubah          ║
║                      gelombang bunyi kepada visual yang memukau.             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import argparse
import warnings
import platform
import subprocess
import shutil
import venv
import matplotlib
import time
import emoji

matplotlib.use('Agg')

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.status import Status
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich import box
from rich.traceback import install

console = Console()
install(show_locals=True)

WARNA = {
    'reset': '\033[0m',
    'merah': '\033[91m',
    'hijau': '\033[92m',
    'kuning': '\033[93m',
    'biru': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'putih': '\033[97m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

FOLDER_VENV = "venv"
NAMA_SKRIP = "penganalisis-gelombang.py"


def emj(nama):
    return emoji.emojize(f":{nama}:", language='alias')


def warna(teks, color='putih', bold=False):
    return f"{WARNA.get(color, WARNA['putih'])}{teks}{WARNA['reset']}"

def print_rich(teks, style=None, bold=False, panel=False, border_style=None):
    if panel:
        console.print(Panel(teks, border_style=border_style or "cyan", box=box.ROUNDED))
    else:
        console.print(teks, style=style)


def detect_platform():
    sistem = platform.system().lower()
    if sistem == 'linux':
        try:
            with open('/proc/1/cgroup', 'r') as f:
                cgroup = f.read()
                if 'android' in cgroup.lower() or 'termux' in cgroup.lower():
                    return 'termux'
        except:
            pass
        return 'linux'
    return sistem


def get_requirements_file():
    plat = detect_platform()
    req_map = {
        'windows': 'requirements_windows.txt',
        'termux': 'requirements_termux.txt',
        'linux': 'requirements_linux.txt'
    }
    return req_map.get(plat, 'requirements_linux.txt')


def semak_dan_setup_venv():
    """Auto-setup virtual environment jika belum ada."""
    if os.path.exists(FOLDER_VENV):
        return True
    
    console.print(Panel.fit(
        "[bold cyan]:person:  Wahai pengguna tercinta, persekitaran virtual sedang disediakan untukmu...[/]",
        border_style="cyan",
        box=box.DOUBLE,
        padding=(1, 2)
    ))
    
    console.print(f"\n  [yellow]:hourglass_flowing_sand:[/] [yellow]Tunggu dengan penuh kesabaran, pustaka sedang dijamu...[/]")
    
    console.print(f"\n  [blue]:gear:[/] Membina persekitaran '[bold]{FOLDER_VENV}[/]'...")
    try:
        venv.create(FOLDER_VENV, with_pip=True)
    except Exception as e:
        console.print(f"  [red]:cross_mark:[/] [red]Ralat Bina: {e}[/]")
        return False
    
    req_file = get_requirements_file()
    platform_detected = detect_platform()
    console.print(f"\n  [cyan]:laptop:[/] Platform dikesan: [bold]{platform_detected}[/]")
    console.print(f"  [cyan]:package:[/] Pasang pustaka dari '[bold]{req_file}[/]'...")
    
    pip_exe = os.path.join(FOLDER_VENV, "Scripts", "pip") if detect_platform() == "windows" else os.path.join(FOLDER_VENV, "bin", "pip")
    
    try:
        subprocess.check_call([pip_exe, "install", "-r", req_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        console.print(f"\n  [green]:check_mark_button:[/] [green]Alangkah cantiknya! Persekitaran telah sedia untukmu.[/]")
        return True
    except Exception as e:
        console.print(f"  [red]:prohibited:[/] [red]Ralat pasang: {e}[/]")
        return False


def cipta_virtual_environment():
    console.print(Panel.fit(
        "[bold cyan]:adhesive_bandage: MEMBINA PERSEKITARAN VIRTUAL[/]",
        border_style="blue",
        box=box.DOUBLE,
        padding=(1, 2)
    ))

    if os.path.exists(FOLDER_VENV):
        console.print(f"\n  [yellow]:warning:[/] Folder '[bold]{FOLDER_VENV}[/]' sudah wujud.")
        respons = input("  [cyan]?[/] Nak bina semula? (y/n): ").strip().lower()
        if respons != 'y':
            console.print(f"\n  [green]:check_mark:[/] Guna persekitaran sedia ada...")
            return True
        console.print(f"\n  [red]:wastebasket:[/] Padam folder lama...")
        shutil.rmtree(FOLDER_VENV)

    console.print(f"\n  [blue]:gear:[/] Membina persekitaran '[bold]{FOLDER_VENV}[/]'...")
    try:
        venv.create(FOLDER_VENV, with_pip=True)
        console.print(f"  [green]:check_mark:[/] [green]Persekitaran virtual telah dicipta![/]")
    except Exception as e:
        console.print(f"  [red]:cross_mark:[/] [red]Ralat: {e}[/]")
        return False

    req_file = get_requirements_file()
    platform_detected = detect_platform()
    console.print(f"\n  [cyan]:laptop:[/] Platform dikesan: [bold]{platform_detected}[/]")
    console.print(f"  [cyan]:package:[/] Pasang pustaka dari '[bold]{req_file}[/]'...")

    pip_exe = os.path.join(FOLDER_VENV, "Scripts", "pip") if detect_platform() == "windows" else os.path.join(FOLDER_VENV, "bin", "pip")

    with console.status(f"[bold cyan]:hourglass_flowing_sand: Sedang pasang pustaka...[/]") as status:
        try:
            subprocess.check_call([pip_exe, "install", "-r", req_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            console.print(f"  [green]:check_mark_button:[/] [green]Semua pustaka telah pasang![/]")
            return True
        except Exception as e:
            console.print(f"  [red]:prohibited:[/] [red]Ralat pasang: {e}[/]")
            return False


PLATFORM_SEMASA = detect_platform()

console.print(Panel.fit(
    f"[bold cyan]:musical_score: PENGANALISIS GELOMBANG[/]\n[dim]Suite Analisis Audio[/]",
    border_style="cyan",
    box=box.DOUBLE,
    padding=(1, 2)
))

table = Table(show_header=False, box=None, pad_edge=False)
table.add_column(style="blue")
table.add_row(f":person: [bold]Penulis[/]   : misyaz-pelitari")
table.add_row(f":calendar: [bold]Versi[/]    : 1.0.0")
table.add_row(f":desktop_computer: [bold]Platform[/] : {PLATFORM_SEMASA}")
console.print(table)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
import librosa
import librosa.display
import soundfile as sf
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

PLOTLY_TERSEDIA = False
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_TERSEDIA = True
except ImportError:
    pass


def konfigurasi_gaya_visual():
    sns.set_style("darkgrid")
    sns.set_context("notebook", font_scale=1.2)
    plt.rcParams.update({
        'figure.figsize': (12, 8),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'legend.fontsize': 10,
        'figure.titleweight': 'bold',
    })


def plot_bentuk_gelombang_3d(y, sr, tempoh, simpan=None, tunjuk=True):
    if not PLOTLY_TERSEDIA:
        return
    masa = np.linspace(0, tempoh, len(y))
    fig = go.Figure(data=[go.Scatter(x=masa, y=y, mode='lines', fill='tozeroy')])
    fig.update_layout(title='Bentuk Gelombang 3D', template='plotly_dark')
    if simpan:
        fig.write_image(simpan.replace('.png', '_3d.png'), width=1400, height=600)
    if tunjuk:
        fig.show()


def plot_spektrogram_3d(y, sr, jenis='mel', simpan=None, tunjuk=True):
    if not PLOTLY_TERSEDIA:
        return
    n_fft, hop_length = 2048, 512
    if jenis == 'mel':
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.power_to_db(S, ref=np.max)
    else:
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig = go.Figure(data=[go.Heatmap(z=S_db, colorscale='Viridis')])
    fig.update_layout(title=f'{jenis.upper()} Spectrogram 3D', template='plotly_dark')
    if simpan:
        fig.write_image(simpan.replace('.png', f'_{jenis}_3d.png'), width=1400, height=700)
    if tunjuk:
        fig.show()


def plot_fitur_delta(y, sr, tempoh, simpan=None, tunjuk=True):
    console.print(f"\n  [cyan]:bar_chart:[/] [bold cyan]Mengekstrak Fitur Delta...[/]")
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfccs)
    mfcc_delta2 = librosa.feature.delta(mfccs, order=2)
    hop_length = 512

    if PLOTLY_TERSEDIA:
        fig = make_subplots(rows=3, cols=1, subplot_titles=('MFCC Asal', 'Delta MFCC', 'Delta-Delta MFCC'))
        for i in range(min(5, mfccs.shape[0])):
            fig.add_trace(go.Heatmap(z=mfccs[:5], colorscale='RdBu', showscale=False), row=1, col=1)
            fig.add_trace(go.Heatmap(z=mfcc_delta[:5], colorscale='RdBu', showscale=False), row=2, col=1)
            fig.add_trace(go.Heatmap(z=mfcc_delta2[:5], colorscale='RdBu', showscale=False), row=3, col=1)
        fig.update_layout(height=900, template='plotly_dark')
        if simpan:
            fig.write_image(simpan.replace('.png', '_delta.png'), width=1400, height=900)
        if tunjuk:
            fig.show()
    else:
        fig, ax = plt.subplots(3, 1, figsize=(14, 12))
        img1 = librosa.display.specshow(mfccs[:5], x_axis='time', sr=sr, ax=ax[0], cmap='coolwarm')
        ax[0].set_title('MFCC Asal')
        fig.colorbar(img1, ax=ax[0])
        img2 = librosa.display.specshow(mfcc_delta[:5], x_axis='time', sr=sr, ax=ax[1], cmap='coolwarm')
        ax[1].set_title('Delta MFCC')
        fig.colorbar(img2, ax=ax[1])
        img3 = librosa.display.specshow(mfcc_delta2[:5], x_axis='time', sr=sr, ax=ax[2], cmap='coolwarm')
        ax[2].set_title('Delta-Delta MFCC')
        fig.colorbar(img3, ax=ax[2])
        fig.suptitle('FITUR DELTA MFCC', fontsize=14, fontweight='bold')
        if simpan:
            fig.savefig(simpan.replace('.png', '_delta.png'), bbox_inches='tight')
        if tunjuk:
            plt.show()
        plt.close(fig)


def plot_fitur_lanjutan(y, sr, tempoh, simpan=None, tunjuk=True):
    console.print(f"\n  [magenta]:bullseye:[/] [bold magenta]Mengekstrak Fitur Terkini...[/]")
    n_fft, hop_length = 2048, 512
    rms = librosa.feature.rms(y=y, frame_length=n_fft, hop_length=hop_length)[0]
    spectral_flatness = librosa.feature.spectral_flatness(y=y, n_fft=n_fft, hop_length=hop_length)[0]
    masa_fitur = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

    fig = plt.figure(figsize=(16, 16))
    gs = gridspec.GridSpec(5, 2, figure=fig, hspace=0.4, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(masa_fitur, rms, color='#e41a1c', linewidth=1.5)
    ax1.fill_between(masa_fitur, rms, 0, color='#e41a1c', alpha=0.3)
    ax1.set_xlabel('Masa (saat)')
    ax1.set_ylabel('RMS')
    ax1.set_title('RMS - Tenaga Audio', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    purata_rms = np.mean(rms)
    ax1.axhline(y=purata_rms, color='blue', linestyle='--', alpha=0.7, label=f'Purata: {purata_rms:.4f}')
    ax1.legend()
    console.print(f"    [green]:check_mark:[/] [green]RMS (purata: {purata_rms:.4f})[/]")

    ax2 = fig.add_subplot(gs[1, :])
    ax2.plot(masa_fitur, spectral_flatness, color='#377eb8', linewidth=1.5)
    ax2.fill_between(masa_fitur, spectral_flatness, 0, color='#377eb8', alpha=0.3)
    ax2.set_xlabel('Masa (saat)')
    ax2.set_ylabel('Spectral Flatness')
    ax2.set_title('Spectral Flatness - Kesejukan Spektrum', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    purata_sf = np.mean(spectral_flatness)
    ax2.axhline(y=purata_sf, color='orange', linestyle='--', alpha=0.7, label=f'Purata: {purata_sf:.4f}')
    ax2.legend()
    console.print(f"    [green]:check_mark:[/] [green]Spectral Flatness (purata: {purata_sf:.4f})[/]")

    chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
    ax3 = fig.add_subplot(gs[2, :])
    img3 = librosa.display.specshow(chroma_cqt, x_axis='time', y_axis='chroma', sr=sr, ax=ax3, cmap='viridis')
    ax3.set_title('Chroma CQT', fontweight='bold')
    fig.colorbar(img3, ax=ax3)
    console.print(f"    [green]:check_mark:[/] [green]Chroma CQT[/]")

    chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
    ax4 = fig.add_subplot(gs[3, :])
    img4 = librosa.display.specshow(chroma_cens, x_axis='time', y_axis='chroma', sr=sr, ax=ax4, cmap='magma')
    ax4.set_title('Chroma CENS', fontweight='bold')
    fig.colorbar(img4, ax=ax4)
    console.print(f"    [green]:check_mark:[/] [green]Chroma CENS[/]")

    poly_features = librosa.feature.poly_features(y=y, sr=sr, order=2)
    ax5 = fig.add_subplot(gs[4, :])
    img5 = librosa.display.specshow(poly_features, x_axis='time', sr=sr, ax=ax5, cmap='plasma')
    ax5.set_title('Poly Features', fontweight='bold')
    ax5.set_ylabel('Pekali')
    fig.colorbar(img5, ax=ax5)
    console.print(f"    [green]:check_mark:[/] [green]Poly Features[/]")

    fig.suptitle('FITUR CANGGIH TERKINI', fontsize=16, fontweight='bold', y=0.98)

    if simpan:
        fig.savefig(simpan.replace('.png', '_fitur_terkini.png'), bbox_inches='tight', pad_inches=0.1)
        console.print(f"\n  [green]:floppy_disk:[/] [green]Simpan: {simpan.replace('.png', '_fitur_terkini.png')}[/]")

    if tunjuk:
        plt.show()
    plt.close(fig)


def muat_audio(laluan, kadar_sasar=22050, mono=True):
    console.print(f"\n  [cyan]:musical_note:[/] [bold]Muatkan audio:[/] {laluan}")
    kadar_sasar = kadar_sasar or 22050
    y, sr = librosa.load(laluan, sr=kadar_sasar, mono=mono)
    tempoh = len(y) / sr

    if tempoh > 300:
        console.print(f"  [yellow]:warning:[/] [yellow]Audio terlalu panjang ({tempoh:.1f}s), potong kepada 300s...[/]")
        y = y[:sr * 300]
        tempoh = 300

    console.print(f"    [green]:antenna_radio:[/] [green]Kadar sampel:[/] {sr} Hz")
    console.print(f"    [green]:stopwatch:[/] [green]Tempoh:[/] {tempoh:.2f} saat")
    console.print(f"    [green]:speaker_high_volume:[/] [green]Saluran:[/] {'Mono' if mono else 'Stereo'}")

    return y, sr, tempoh


def plot_bentuk_gelombang(y, sr, tempoh, judul="Bentuk Gelombang Suara", simpan=None, tunjuk=True):
    masa = np.linspace(0, tempoh, len(y))
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(masa, y, color='#1f77b4', linewidth=0.5, alpha=0.8)
    ax.fill_between(masa, y, 0, where=(y > 0), color='#1f77b4', alpha=0.3)
    ax.fill_between(masa, y, 0, where=(y < 0), color='#d62728', alpha=0.3)
    ax.set_xlabel("Masa (saat)", fontweight='bold')
    ax.set_ylabel("Amplitud", fontweight='bold')
    ax.set_title(judul, fontweight='bold', pad=20)
    ax.set_xlim(0, tempoh)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.axhline(y=0, color='black', linewidth=0.8, alpha=0.5)

    def format_masa(x, pos):
        return f"{x:.1f}s"
    ax.xaxis.set_major_formatter(FuncFormatter(format_masa))

    if simpan:
        fig.savefig(simpan, bbox_inches='tight', pad_inches=0.1)
        console.print(f"  [green]:floppy_disk:[/] [green]Simpan:[/] {simpan}")

    if tunjuk:
        plt.show()
    plt.close(fig)


def plot_spektrogram(y, sr, judul="Spektrogram", jenis='mel', simpan=None, tunjuk=True):
    n_fft, hop_length = 2048, 512
    fig, ax = plt.subplots(figsize=(14, 6))

    if jenis == 'mel':
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.power_to_db(S, ref=np.max)
        img = librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel', ax=ax, cmap='viridis')
        ax.set_ylabel('Frekuensi (Mel)')
        nama = "Mel-Spektrogram"
    elif jenis == 'linear':
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        img = librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='linear', ax=ax, cmap='viridis')
        ax.set_ylabel('Frekuensi (Hz)')
        nama = "Spektrogram Linear"
    else:
        D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        img = librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log', ax=ax, cmap='viridis')
        ax.set_ylabel('Frekuensi (Hz, skala log)')
        nama = "Spektrogram Logaritmik"

    cbar = fig.colorbar(img, ax=ax, format='%+2.0f dB')
    cbar.set_label('Keamatan (dB)', rotation=270, labelpad=20, fontweight='bold')
    ax.set_xlabel('Masa (saat)', fontweight='bold')
    ax.set_title(f"{judul}\n({nama})", fontweight='bold', pad=20)

    if simpan:
        nama_fail, ext = os.path.splitext(simpan)
        fail_spektro = f"{nama_fail}_{jenis}{ext}"
        fig.savefig(fail_spektro, bbox_inches='tight', pad_inches=0.1)
        console.print(f"  [green]:floppy_disk:[/] [green]Simpan:[/] {fail_spektro}")

    if tunjuk:
        plt.show()
    plt.close(fig)


def plot_fitur_canggih(y, sr, tempoh, simpan=None, tunjuk=True):
    console.print(f"\n  [magenta]:microscope:[/] [bold magenta]Mengekstrak Fitur Canggung...[/]")

    fig = plt.figure(figsize=(16, 20))
    gs = gridspec.GridSpec(7, 2, figure=fig, width_ratios=[3, 1],
        height_ratios=[1, 1, 1, 1, 1, 1, 1], hspace=0.4, wspace=0.3)

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    ax1 = fig.add_subplot(gs[0, 0])
    img1 = librosa.display.specshow(mfccs, x_axis='time', sr=sr, ax=ax1, cmap='coolwarm')
    ax1.set_title('MFCC', fontweight='bold')
    ax1.set_ylabel('Pekali MFCC')
    fig.colorbar(img1, ax=ax1, format='%.1f')

    ax1b = fig.add_subplot(gs[0, 1])
    purata_mfcc = np.mean(mfccs, axis=1)
    ax1b.barh(np.arange(len(purata_mfcc)), purata_mfcc, color=plt.cm.coolwarm(np.linspace(0, 1, len(purata_mfcc))))
    ax1b.set_xlabel('Nilai Purata')
    ax1b.set_title('Purata MFCC')
    ax1b.grid(True, alpha=0.3)
    console.print(f"    [green]:check_mark:[/] [green]MFCC (13 pekali)[/]")

    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    ax2 = fig.add_subplot(gs[1, 0])
    img2 = librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', sr=sr, ax=ax2, cmap='viridis')
    ax2.set_title('Kromagram', fontweight='bold')
    fig.colorbar(img2, ax=ax2)

    ax2b = fig.add_subplot(gs[1, 1])
    purata_chroma = np.mean(chroma, axis=1)
    nama_nada = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    ax2b.barh(nama_nada, purata_chroma, color=plt.cm.viridis(np.linspace(0, 1, 12)))
    ax2b.set_xlabel('Keamatan Purata')
    ax2b.set_title('Taburan Nada')
    ax2b.grid(True, alpha=0.3)
    console.print(f"    [green]:check_mark:[/] [green]Kromagram (12 nada)[/]")

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    masa_fitur = librosa.frames_to_time(np.arange(len(centroid)), sr=sr)

    ax3 = fig.add_subplot(gs[2, :])
    ax3.plot(masa_fitur, centroid, color='#e41a1c', linewidth=2)
    ax3.fill_between(masa_fitur, centroid, 0, color='#e41a1c', alpha=0.2)
    ax3.set_xlabel('Masa (saat)', fontweight='bold')
    ax3.set_ylabel('Frekuensi (Hz)', fontweight='bold')
    ax3.set_title('Sentroid Spektrum', fontweight='bold')
    ax3.set_xlim(0, tempoh)
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=np.mean(centroid), color='blue', linestyle='--', alpha=0.7, label=f'Purata: {np.mean(centroid):.0f} Hz')
    ax3.legend()
    console.print(f"    [green]:check_mark:[/] [green]Sentroid Spektrum (purata: {np.mean(centroid):.0f} Hz)[/]")

    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    ax4 = fig.add_subplot(gs[3, :])
    ax4.plot(masa_fitur, bandwidth, color='#377eb8', linewidth=2)
    ax4.fill_between(masa_fitur, bandwidth, 0, color='#377eb8', alpha=0.2)
    ax4.set_xlabel('Masa (saat)', fontweight='bold')
    ax4.set_ylabel('Lebar Jalur (Hz)', fontweight='bold')
    ax4.set_title('Lebar Jalur Spektrum', fontweight='bold')
    ax4.set_xlim(0, tempoh)
    ax4.grid(True, alpha=0.3)
    console.print(f"    [green]:check_mark:[/] [green]Lebar Jalur Spektrum (purata: {np.mean(bandwidth):.0f} Hz)[/]")

    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    ax5 = fig.add_subplot(gs[4, :])
    ax5.plot(masa_fitur, rolloff, color='#4daf4a', linewidth=2)
    ax5.fill_between(masa_fitur, rolloff, 0, color='#4daf4a', alpha=0.2)
    ax5.set_xlabel('Masa (saat)', fontweight='bold')
    ax5.set_ylabel('Frekuensi (Hz)', fontweight='bold')
    ax5.set_title('Rolloff Spektrum', fontweight='bold')
    ax5.set_xlim(0, tempoh)
    ax5.grid(True, alpha=0.3)
    console.print(f"    [green]:check_mark:[/] [green]Rolloff Spektrum (purata: {np.mean(rolloff):.0f} Hz)[/]")

    zcr = librosa.feature.zero_crossing_rate(y)[0]
    ax6 = fig.add_subplot(gs[5, :])
    ax6.plot(masa_fitur, zcr, color='#984ea3', linewidth=2)
    ax6.fill_between(masa_fitur, zcr, 0, color='#984ea3', alpha=0.2)
    ax6.set_xlabel('Masa (saat)', fontweight='bold')
    ax6.set_ylabel('Kadar Lintas Sifar', fontweight='bold')
    ax6.set_title('Kadar Lintas Sifar (ZCR)', fontweight='bold')
    ax6.set_xlim(0, tempoh)
    ax6.grid(True, alpha=0.3)
    console.print(f"    [green]:check_mark:[/] [green]Kadar Lintas Sifar (purata: {np.mean(zcr):.3f})[/]")

    y_harmonik, y_perkusif = librosa.effects.hpss(y)
    ax7 = fig.add_subplot(gs[6, :])
    masa = np.linspace(0, tempoh, len(y))
    ax7.plot(masa, y_harmonik, color='#ff7f00', linewidth=0.8, alpha=0.8, label='Harmonik (Melodi)')
    ax7.plot(masa, y_perkusif, color='#a65628', linewidth=0.8, alpha=0.8, label='Perkusif (Rentak)')
    ax7.set_xlabel('Masa (saat)', fontweight='bold')
    ax7.set_ylabel('Amplitud', fontweight='bold')
    ax7.set_title('Pembahagian Harmonik-Perkusif (HPSS)', fontweight='bold')
    ax7.set_xlim(0, tempoh)
    ax7.grid(True, alpha=0.3)
    ax7.legend(loc='upper right')
    console.print(f"    [green]:check_mark:[/] [green]Pembahagian Harmonik-Perkusif[/]")

    fig.suptitle('FITUR CANGGIH PENGANALISIS GELOMBANG', fontsize=18, fontweight='bold', y=0.98)

    if simpan:
        fail_fitur = simpan.replace('.png', '_fitur_canggih.png')
        fig.savefig(fail_fitur, bbox_inches='tight', pad_inches=0.1)
        console.print(f"\n  [green]:floppy_disk:[/] [green]Simpan:[/] {fail_fitur}")

    if tunjuk:
        plt.show()
    plt.close(fig)


def plot_analisis_lanjutan(y, sr, tempoh, simpan=None, tunjuk=True):
    console.print(f"\n  [magenta]:rocket:[/] [bold magenta]Menjalankan Analisis Lanjutan...[/]")

    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True, units='frames')
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    ax1 = fig.add_subplot(gs[0, :])
    masa = np.linspace(0, tempoh, len(y))
    ax1.plot(masa, y, color='#1f77b4', linewidth=0.5, alpha=0.7)
    for t in onset_times:
        ax1.axvline(x=t, color='red', alpha=0.5, linewidth=1, linestyle='--')
    ax1.set_xlabel('Masa (saat)', fontweight='bold')
    ax1.set_ylabel('Amplitud', fontweight='bold')
    ax1.set_title(f'Pengesanan Onset ({len(onset_times)} onset)', fontweight='bold')
    ax1.set_xlim(0, tempoh)
    ax1.grid(True, alpha=0.3)
    console.print(f"    [green]:check_mark:[/] [green]Pengesanan Onset: {len(onset_times)} onset[/]")

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    tempo = float(tempo[0]) if isinstance(tempo, np.ndarray) and len(tempo) > 0 else (float(tempo) if isinstance(tempo, (int, float)) else 0.0)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    masa_onset = librosa.times_like(onset_env, sr=sr)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(masa_onset, onset_env, color='#2ca02c', linewidth=1.5, label='Kekuatan Onset')
    for bt in beat_times:
        ax2.axvline(x=bt, color='orange', alpha=0.4, linewidth=0.8)
    ax2.set_xlabel('Masa (saat)', fontweight='bold')
    ax2.set_ylabel('Kekuatan Onset', fontweight='bold')
    ax2.set_title(f'Penjejakan Rentak - Tempo: {tempo:.1f} BPM', fontweight='bold')
    ax2.set_xlim(0, tempoh)
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    ax3 = fig.add_subplot(gs[1, 1])
    tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
    img3 = librosa.display.specshow(tempogram, sr=sr, x_axis='time', y_axis='tempo', ax=ax3, cmap='magma')
    ax3.set_title('Tempogram', fontweight='bold')
    ax3.set_ylabel('Tempo (BPM)')
    fig.colorbar(img3, ax=ax3, format='%.2f')
    console.print(f"    [green]:check_mark:[/] [green]Penjejakan Rentak: {tempo:.1f} BPM, {len(beat_times)} rentak[/]")

    kontras = librosa.feature.spectral_contrast(y=y, sr=sr)
    ax4 = fig.add_subplot(gs[2, 0])
    img4 = librosa.display.specshow(kontras, x_axis='time', sr=sr, ax=ax4, cmap='RdBu_r')
    ax4.set_title('Kontras Spektrum', fontweight='bold')
    ax4.set_ylabel('Jalur Frekuensi')
    fig.colorbar(img4, ax=ax4, format='%.1f')

    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    ax5 = fig.add_subplot(gs[2, 1])
    img5 = librosa.display.specshow(tonnetz, x_axis='time', sr=sr, ax=ax5, cmap='plasma')
    ax5.set_title('Tonnetz', fontweight='bold')
    ax5.set_ylabel('Dimensi Tonnetz')
    fig.colorbar(img5, ax=ax5, format='%.2f')
    console.print(f"    [green]:check_mark:[/] [green]Kontras Spektrum & Tonnetz[/]")

    fig.suptitle('ANALISIS LANJUTAN', fontsize=16, fontweight='bold', y=0.98)

    if simpan:
        fail_lanjutan = simpan.replace('.png', '_analisis_lanjutan.png')
        fig.savefig(fail_lanjutan, bbox_inches='tight', pad_inches=0.1)
        console.print(f"\n  [green]:floppy_disk:[/] [green]Simpan:[/] {fail_lanjutan}")

    if tunjuk:
        plt.show()
    plt.close(fig)


def analisis_penuh(laluan_audio, folder_output="hasil_analisis"):
    os.makedirs(folder_output, exist_ok=True)
    nama_fail = os.path.splitext(os.path.basename(laluan_audio))[0]
    awalan_output = os.path.join(folder_output, nama_fail)

    console.print(f"\n[cyan]═{'═'*58}[/]")
    console.print(f"  [bold cyan]:musical_score:[/] [bold cyan]PENGANALISIS GELOMBANG - ANALISIS PENUH[/]")
    console.print(f"[cyan]═{'═'*58}[/]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task_muat = progress.add_task("[cyan]:musical_note: Muatkan audio...", total=None)
        y, sr, tempoh = muat_audio(laluan_audio)
        progress.update(task_muat, completed=True)

        task_gelombang = progress.add_task("[blue]:water_wave: Lukis Bentuk Gelombang...", total=100)
        plot_bentuk_gelombang(y, sr, tempoh, simpan=f"{awalan_output}_bentuk_gelombang.png", tunjuk=False)
        progress.update(task_gelombang, completed=100)

        task_spektro = progress.add_task("[blue]:artist_palette: Lukis Spektrogram...", total=100)
        for i, jenis in enumerate(['mel', 'linear', 'log']):
            plot_spektrogram(y, sr, jenis=jenis, simpan=f"{awalan_output}_spektrogram.png", tunjuk=False)
            progress.update(task_spektro, completed=((i+1) / 3) * 100)

        task_canggih = progress.add_task("[magenta]:microscope: Ekstrak Fitur Canggang...", total=100)
        plot_fitur_canggih(y, sr, tempoh, simpan=f"{awalan_output}.png", tunjuk=False)
        progress.update(task_canggih, completed=100)

        task_lanjutan = progress.add_task("[magenta]:rocket: Analisis Lanjutan...", total=100)
        plot_analisis_lanjutan(y, sr, tempoh, simpan=f"{awalan_output}.png", tunjuk=False)
        progress.update(task_lanjutan, completed=100)

        if PLOTLY_TERSEDIA:
            task_delta = progress.add_task("[yellow]:bar_chart: Ekstrak Fitur Delta...", total=100)
            plot_fitur_delta(y, sr, tempoh, simpan=f"{awalan_output}_delta.png", tunjuk=False)
            progress.update(task_delta, completed=100)

        task_terkini = progress.add_task("[yellow]:bullseye: Ekstrak Fitur Terkini...", total=100)
        plot_fitur_lanjutan(y, sr, tempoh, simpan=f"{awalan_output}.png", tunjuk=False)
        progress.update(task_terkini, completed=100)

        if PLOTLY_TERSEDIA:
            task_3d = progress.add_task("[yellow]:rainbow: Visual 3D Interaktif...", total=100)
            plot_bentuk_gelombang_3d(y, sr, tempoh, simpan=f"{awalan_output}_3d.png", tunjuk=False)
            progress.update(task_3d, completed=100)

    console.print(f"\n[cyan]═{'═'*58}[/]")
    console.print(f"  [bold green]:check_mark_button:[/] [bold green]ANALISIS SELESAI![/]")
    console.print(f"  [green]:file_folder:[/] [green]Folder output: {folder_output}/[/]")
    console.print(f"[cyan]═{'═'*58}[/]")

    rms = librosa.feature.rms(y=y)[0]
    spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]

    with open(f"{awalan_output}_ringkasan.txt", "w", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write(" RINGKASAN ANALISIS AUDIO\n")
        f.write("="*50 + "\n\n")
        f.write(f":file_folder: Fail Audio    : {laluan_audio}\n")
        f.write(f":antenna_radio: Kadar Sampel  : {sr} Hz\n")
        f.write(f":stopwatch: Tempoh        : {tempoh:.2f} saat\n")
        f.write(f":bar_chart: Bilangan Sampel: {len(y)}\n")
        f.write(f":desktop_computer: Platform     : {PLATFORM_SEMASA}\n\n")
        f.write("-"*30 + "\n")
        f.write(" STATISTIK ASAS\n")
        f.write("-"*30 + "\n")
        f.write(f":chart_increasing: Amplitud Maksimum: {np.max(y):.4f}\n")
        f.write(f":chart_decreasing: Amplitud Minimum : {np.min(y):.4f}\n")
        f.write(f":bar_chart: Amplitud Purata  : {np.mean(y):.4f}\n")
        f.write(f":straight_ruler: Sisihan Piawai   : {np.std(y):.4f}\n")
        f.write(f":high_voltage: Tenaga (RMS)     : {np.mean(rms):.4f}\n")
        f.write(f":snowflake: Spectral Flatness: {np.mean(spectral_flatness):.4f}\n")

    console.print(f"  [green]:memo:[/] [green]Ringkasan: {awalan_output}_ringkasan.txt[/]")


def paparkan_menu():
    table = Table(title="[bold cyan]:clipboard: MENU UTAMA[/]", show_header=False, box=box.ROUNDED)
    table.add_column("No", style="cyan", justify="center")
    table.add_column("Pilihan", style="bold")
    table.add_column("Huraian", style="dim")

    table.add_row("1", "[blue]:musical_note:[/] [blue]Analisis Penuh[/]", "Semua visualisasi")
    table.add_row("2", "[cyan]:water_wave:[/] [cyan]Bentuk Gelombang[/]", "Plot waves audio")
    table.add_row("3", "[cyan]:artist_palette:[/] [cyan]Spektrogram[/]", "Spektrogram (mel/linear/log)")
    table.add_row("4", "[magenta]:microscope:[/] [magenta]Fitur Canggih[/]", "MFCC, Kromagram, Sentroid, dll")
    table.add_row("5", "[magenta]:rocket:[/] [magenta]Analisis Lanjutan[/]", "Onset, Beat, Tempo")
    table.add_row("6", "[red]:bar_chart:[/] [red]Fitur Delta[/]", "MFCC + Delta + Delta-Delta")
    table.add_row("7", "[red]:bullseye:[/] [red]Fitur Terkini[/]", "RMS, Spectral Flatness, dll")
    table.add_row("8", "[red]:rainbow:[/] [red]Visual 3D Interaktif[/]", "Plotly Interactive")
    table.add_row("", "", "")
    table.add_row("[yellow]S[/]", "[yellow]:gear:[/] [yellow]Setup Virtual Environment[/]", "Cipta persekitaran venv")
    table.add_row("[yellow]I[/]", "[yellow]:information:[/] [yellow]Maklumat[/]", "Info lanjut projek")
    table.add_row("[yellow]B[/]", "[yellow]:question_mark:[/] [yellow]Bantuan[/]", "Guide penggunaan")
    table.add_row("[red]Q[/]", "[red]:door:[/] [red]Keluar[/]", "Tamat program")

    console.print(table)


def paparkan_maklumat():
    console.print(Panel.fit(
        "[bold cyan]:musical_score: PENGANALISIS GELOMBANG[/]\n[dim]Penukar Suara Kepada Lukisan Visual[/]",
        border_style="cyan",
        box=box.DOUBLE,
        padding=(1, 2)
    ))

    info_table = Table(show_header=False, box=None)
    info_table.add_column(style="bold")
    info_table.add_row(":person: [bold]Penulis[/]      : misyaz-pelitari")
    info_table.add_row(":calendar: [bold]Versi[/]       : 1.0.0")
    info_table.add_row(f":desktop_computer: [bold]Platform[/]    : {PLATFORM_SEMASA}")
    info_table.add_row(f":calendar: [bold]Tarikh[/]      : {time.strftime('%d-%m-%Y')}")
    console.print(info_table)

    keistimewaan_table = Table(title="[bold]:package: KEISTIMEWAAN[/]", box=box.ROUNDED)
    keistimewaan_table.add_column("Status", justify="center", style="green")
    keistimewaan_table.add_column("Huraian", style="dim")
    keistimewaan_table.add_row(":check_mark:", "Pengesanan Automatik Platform (Windows/Linux/Termux)")
    keistimewaan_table.add_row(":check_mark:", "Visualisasi 3D Interaktif (Plotly)")
    keistimewaan_table.add_row(":check_mark:", "Fitur Delta MFCC (Terbitan Pertama & Kedua)")
    keistimewaan_table.add_row(":check_mark:", "Palet Warna Istimewa")
    keistimewaan_table.add_row(":check_mark:", "RMS, Spectral Flatness, Chroma CQT/CENS, Poly Features")
    keistimewaan_table.add_row(":check_mark:", "Simpanan Automatik")
    keistimewaan_table.add_row(":check_mark:", "Ringkasan Teks")
    keistimewaan_table.add_row(":check_mark:", "Sokongan Multi Format Audio (WAV, MP3, FLAC, OGG)")
    console.print(keistimewaan_table)

    fitur_table = Table(title="[bold]:books: FITUR YANG TERSEDIA[/]", box=box.ROUNDED)
    fitur_table.add_column("Bil", justify="center", style="cyan")
    fitur_table.add_column("Senarai Fitur", style="dim")
    fitur_table.add_row("1", "Bentuk Gelombang • Spektrogram (3 Jenis) • MFCC (13 Pekali)")
    fitur_table.add_row("2", "Kromagram (12 Nada) • Sentroid Spektrum • Lebar Jalur")
    fitur_table.add_row("3", "Rolloff Spektrum • Kadar Lintas Sifar • HPSS")
    fitur_table.add_row("4", "Onset Detection • Beat Tracking • Tempogram")
    fitur_table.add_row("5", "Kontras Spektrum • Tonnetz • Chroma CQT/CENS")
    fitur_table.add_row("6", "RMS • Spectral Flatness • Poly Features")
    fitur_table.add_row("7", "Plot 3D Interaktif")
    console.print(fitur_table)


def paparkan_bantuan():
    console.print(Panel.fit(
        "[bold yellow]:question_mark: BANTUAN[/]",
        border_style="yellow",
        box=box.DOUBLE,
        padding=(1, 2)
    ))

    console.print("\n[bold]CARA PENGGUNAAN:[/]")
    console.print("[green]$[/] [green]python penganalisis-gelombang.py <audio> [options][/]")

    contoh_table = Table(title="[bold]CONTOH[/]", box=box.ROUNDED)
    contoh_table.add_column("Perintah", style="cyan")
    contoh_table.add_column("Huraian", style="dim")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --penuh", "Analisis penuh")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --bentuk-gelombang", "Bentuk gelombang")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --spektrogram mel", "Spektrogram Mel")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --fitur", "Fitur canggih")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --lanjutan", "Analisis lanjutan")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --visual3d", "Visual 3D")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --delta", "Fitur Delta MFCC")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --canggih", "Fitur terkini")
    contoh_table.add_row("python penganalisis-gelombang.py audio.wav --penuh -o hasil/", "Output folder")
    console.print(contoh_table)

    opsi_table = Table(title="[bold]OPSI[/]", box=box.ROUNDED)
    opsi_table.add_column("Opsi", style="cyan")
    opsi_table.add_column("Huraian", style="dim")
    opsi_table.add_row("--penuh", "Analisis penuh (semua visualisasi)")
    opsi_table.add_row("--bentuk-gelombang", "Plot bentuk gelombang")
    opsi_table.add_row("--spektrogram", "Plot spektrogram (mel/linear/log)")
    opsi_table.add_row("--fitur", "Plot fitur canggih")
    opsi_table.add_row("--lanjutan", "Analisis lanjutan")
    opsi_table.add_row("--visual3d", "Visual 3D interaktif")
    opsi_table.add_row("--delta", "Fitur Delta MFCC")
    opsi_table.add_row("--canggih", "Fitur terkini")
    opsi_table.add_row("-o, --output", "Folder output (lalai: hasil_analisis)")
    opsi_table.add_row("--setup-venv", "Cipta virtual environment")
    console.print(opsi_table)

    console.print("\n[bold]MAKLUMAT LANJUT:[/]")
    console.print("  [cyan]--maklumat[/]   : Paparkan maklumat projek")
    console.print("  [cyan]--menu[/]       : Paparkan menu interaktif")
    console.print("  [cyan]--bantuan[/]    : Paparkan bantuan ini")


def paparkan_submenu_analisis():
    console.print(Panel.fit(
        "[bold green]:check_mark_button: ANALISIS SELESAI[/]",
        border_style="green",
        box=box.DOUBLE,
        padding=(1, 2)
    ))
    
    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_column("Pilihan", style="bold", justify="center")
    table.add_column("Huraian", style="dim")
    table.add_row("[cyan]K[/]", "Kembali ke Menu Utama")
    table.add_row("[cyan]U[/]", "Ulang analisis dengan fail yang sama")
    table.add_row("[cyan]P[/]", "Pilihan Baharu - Pilih fail audio baharu")
    console.print(table)


def jalankan_analisis(args):
    konfigurasi_gaya_visual()
    
    if not os.path.exists(args.audio):
        console.print(f"\n  [red]:prohibited:[/] [red]Maaf, fail '{args.audio}' tidak dijumpai![/]")
        return False
    
    os.makedirs(args.output, exist_ok=True)
    
    if not (args.bentuk_gelombang or args.spektrogram or args.fitur or
           args.lanjutan or args.penuh):
        args.penuh = True
    
    if args.penuh:
        analisis_penuh(args.audio, args.output)
        return True
    
    y, sr, tempoh = muat_audio(args.audio)
    nama_fail = os.path.splitext(os.path.basename(args.audio))[0]
    awalan = os.path.join(args.output, nama_fail)
    
    if args.bentuk_gelombang:
        console.print(f"\n  [blue]:water_wave:[/] [bold blue]Melukis Bentuk Gelombang...[/]")
        plot_bentuk_gelombang(y, sr, tempoh, simpan=f"{awalan}_bentuk_gelombang.png", tunjuk=True)
    
    if args.spektrogram:
        console.print(f"\n  [blue]:artist_palette:[/] [bold blue]Melukis Spektrogram ({args.spektrogram})...[/]")
        plot_spektrogram(y, sr, jenis=args.spektrogram, simpan=f"{awalan}_spektrogram.png", tunjuk=True)
    
    if args.fitur:
        console.print(f"\n  [magenta]:microscope:[/] [bold magenta]Mengekstrak Fitur Canggang...[/]")
        plot_fitur_canggih(y, sr, tempoh, simpan=f"{awalan}.png", tunjuk=True)
    
    if args.lanjutan:
        console.print(f"\n  [magenta]:rocket:[/] [bold magenta]Menjalankan Analisis Lanjutan...[/]")
        plot_analisis_lanjutan(y, sr, tempoh, simpan=f"{awalan}.png", tunjuk=True)
    
    if args.delta:
        console.print(f"\n  [red]:bar_chart:[/] [bold red]Melukis Fitur Delta...[/]")
        plot_fitur_delta(y, sr, tempoh, simpan=f"{awalan}_delta.png", tunjuk=True)
    
    if args.canggih:
        console.print(f"\n  [red]:bullseye:[/] [bold red]Melukis Fitur Terkini...[/]")
        plot_fitur_lanjutan(y, sr, tempoh, simpan=f"{awalan}.png", tunjuk=True)
    
    if args.visual3d:
        console.print(f"\n  [red]:rainbow:[/] [bold red]Melukis Visual 3D Interaktif...[/]")
        plot_bentuk_gelombang_3d(y, sr, tempoh, simpan=f"{awalan}_3d.png", tunjuk=True)
    
    console.print(f"\n  [green]:check_mark_button:[/] [bold green]Analisis selesai! Folder: {args.output}/[/]")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="[bold cyan]:musical_score:[/] [cyan]PENGANALISIS GELOMBANG[/] - Penukar Suara Kepada Lukisan Visual",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CONTOH PENGGUNAAN                                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  python penganalisis-gelombang.py audio.wav --penuh                          ║
║  python penganalisis-gelombang.py audio.wav --bentuk-gelombang               ║
║  python penganalisis-gelombang.py audio.wav --spektrogram mel                ║
║  python penganalisis-gelombang.py audio.wav --fitur                          ║
║  python penganalisis-gelombang.py audio.wav --lanjutan                       ║
║  python penganalisis-gelombang.py audio.wav --penuh -o hasil/                ║
║  python penganalisis-gelombang.py --setup-venv                               ║
║  python penganalisis-gelombang.py --menu                                     ║
║  python penganalisis-gelombang.py --bantuan                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    )

    parser.add_argument("--menu", action="store_true", help="Paparkan menu interaktif")
    parser.add_argument("--maklumat", action="store_true", help="Paparkan maklumat projek")
    parser.add_argument("--bantuan", action="store_true", help="Paparkan bantuan")
    parser.add_argument("--setup-venv", action="store_true", help="Cipta virtual environment")
    parser.add_argument("audio", nargs="?", help="Fail audio (WAV, MP3, FLAC, OGG)")
    parser.add_argument("-o", "--output", default="hasil_analisis", help="Folder output")
    parser.add_argument("--bentuk-gelombang", action="store_true", help="Plot bentuk gelombang")
    parser.add_argument("--spektrogram", choices=['mel', 'linear', 'log'], help="Plot spektrogram")
    parser.add_argument("--fitur", action="store_true", help="Plot fitur canggih")
    parser.add_argument("--lanjutan", action="store_true", help="Analisis lanjutan")
    parser.add_argument("--visual3d", action="store_true", help="Visual 3D interaktif")
    parser.add_argument("--delta", action="store_true", help="Fitur Delta MFCC")
    parser.add_argument("--canggih", action="store_true", help="Fitur terkini")
    parser.add_argument("--penuh", action="store_true", help="Analisis penuh")

    args = parser.parse_args()

    if not args.setup_venv and not args.maklumat and not args.bantuan:
        semak_dan_setup_venv()

    if args.menu:
        paparkan_menu()
        while True:
            pilihan = input(f"\n  [bold cyan]>[/] [bold]Harap pilih pilihan anda:[/] ").strip().lower()
            if pilihan == 'q' or pilihan == 'keluar':
                console.print(f"\n  [cyan]:waving_hand:[/] [bold cyan]Selamat tinggal! Hingga jumpa lagi.[/]")
                break
            elif pilihan == 'i' or pilihan == 'maklumat':
                paparkan_maklumat()
            elif pilihan == 'b' or pilihan == 'bantuan':
                paparkan_bantuan()
            elif pilihan == 's' or pilihan == 'setup':
                cipta_virtual_environment()
            elif pilihan in ['1', '2', '3', '4', '5', '6', '7', '8']:
                while True:
                    if not args.audio:
                        console.print(f"\n  [red]:prohibited:[/] [red]Wahai pengguna tercinta, sila pilih fail audio kesukaan anda![/]")
                        args.audio = input(f"  [bold cyan]>[/] [bold]Masukkan laluan fail audio:[/] ").strip()
                    if not os.path.exists(args.audio):
                        console.print(f"\n  [red]:prohibited:[/] [red]Maaf, segalahalla telah hilang... fail '{args.audio}' tidak jumpa![/]")
                        args.audio = None
                        continue
                    
                    pilihan_map = {
                        '1': 'penuh', '2': 'bentuk-gelombang', '3': 'spektrogram',
                        '4': 'fitur', '5': 'lanjutan', '6': 'delta',
                        '7': 'canggih', '8': 'visual3d'
                    }
                    
                    console.print(f"\n  [cyan]:musical_note:[/] [bold cyan]Wahai pengguna tercinta, fail audio yang dipilih:[/] {args.audio}")
                    setattr(args, pilihan_map[pilihan], True)
                    
                    if not (args.bentuk_gelombang or args.spektrogram or args.fitur or
                           args.lanjutan or args.delta or args.canggih or args.visual3d or args.penuh):
                        args.penuh = True
                    
                    jalankan_analisis(args)
                    paparkan_submenu_analisis()
                    
                    while True:
                        sub_pilihan = input(f"\n  [bold cyan]>[/] [bold]Harap pilih dengan bijaksana:[/] ").strip().lower()
                        if sub_pilihan == 'k':
                            for key in pilihan_map.values():
                                if hasattr(args, key):
                                    setattr(args, key, False)
                            break
                        elif sub_pilihan == 'u':
                            for key in pilihan_map.values():
                                if hasattr(args, key):
                                    setattr(args, key, False)
                            setattr(args, pilihan_map[pilihan], True)
                            jalankan_analisis(args)
                            paparkan_submenu_analisis()
                            continue
                        elif sub_pilihan == 'p':
                            args.audio = None
                            for key in pilihan_map.values():
                                if hasattr(args, key):
                                    setattr(args, key, False)
                            break
                        else:
                            console.print(f"\n  [yellow]:warning:[/] [yellow]Pilihan tidak sah. Sila pilih K, U, atau P.[/]")
                    
                    if sub_pilihan == 'k':
                        continue
                    
                    if sub_pilihan == 'p':
                        continue
            else:
                console.print(f"\n  [yellow]:warning:[/] [yellow]Pilihan tidak sah. Cuba lagi dengan bijaksana.[/]")

    if args.maklumat:
        paparkan_maklumat()
        return

    if args.bantuan:
        paparkan_bantuan()
        return

    if args.setup_venv:
        cipta_virtual_environment()
        return

    if not args.audio:
        paparkan_menu()
        return

    jalankan_analisis(args)


if __name__ == "__main__":
    main()