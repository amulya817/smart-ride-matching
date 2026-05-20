"""
algorithms/visualization.py
----------------------------
Matplotlib-based visualisation helpers used by the Streamlit pages.
These functions were previously inlined in app.py; they are extracted here
so that individual pages can import them independently.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe


# ---------------------------------------------------------------------------
# Route Map
# ---------------------------------------------------------------------------

def draw_route(driver_loc, pickup, destination, pickup_path, trip_path, grid_size=20):
    """Return a Matplotlib Figure showing the driver → pickup → destination route."""
    fig, ax = plt.subplots(figsize=(9, 9), dpi=100)
    fig.patch.set_facecolor("#0a0a14")
    ax.set_facecolor("#0a0a14")

    # Checkerboard background
    for i in range(grid_size):
        for j in range(grid_size):
            if (i + j) % 2 == 0:
                ax.add_patch(plt.Rectangle(
                    (i - 0.5, j - 0.5), 1, 1,
                    facecolor=(25 / 255, 15 / 255, 40 / 255, 0.4),
                    edgecolor="none", zorder=0
                ))

    for i in range(grid_size):
        ax.axhline(y=i, color="#1a1525", linewidth=0.3, zorder=1)
        ax.axvline(x=i, color="#1a1525", linewidth=0.3, zorder=1)

    # Paths
    if pickup_path and len(pickup_path) > 1:
        ppx = [p[0] for p in pickup_path]
        ppy = [p[1] for p in pickup_path]
        ax.plot(ppx, ppy, color="#a855f7", linewidth=8, alpha=0.1, zorder=2, solid_capstyle="round")
        ax.plot(ppx, ppy, color="#a855f7", linewidth=3, alpha=0.9, zorder=3, solid_capstyle="round")

    if trip_path and len(trip_path) > 1:
        ttx = [p[0] for p in trip_path]
        tty = [p[1] for p in trip_path]
        ax.plot(ttx, tty, color="#ec4899", linewidth=8, alpha=0.1, zorder=2, solid_capstyle="round")
        ax.plot(ttx, tty, color="#ec4899", linewidth=3, alpha=0.9, zorder=3, solid_capstyle="round")

    def _add_arrows(path, color):
        step = max(len(path) // 4, 2)
        for i in range(step, len(path), step):
            ddx = path[i][0] - path[i - 1][0]
            ddy = path[i][1] - path[i - 1][1]
            if ddx == 0 and ddy == 0:
                continue
            ax.annotate(
                "", xy=(path[i][0], path[i][1]),
                xytext=(path[i - 1][0], path[i - 1][1]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=13),
                zorder=4
            )

    if pickup_path and len(pickup_path) > 2:
        _add_arrows(pickup_path, "#a855f7")
    if trip_path and len(trip_path) > 2:
        _add_arrows(trip_path, "#ec4899")

    # Glow rings
    for loc, color in [(driver_loc, "#10b981"), (pickup, "#ec4899"), (destination, "#a855f7")]:
        circle = plt.Circle(loc, 1.2, facecolor=color, alpha=0.06,
                            edgecolor=color, linewidth=0.8, linestyle="--", zorder=2)
        ax.add_patch(circle)

    mpe = [pe.withStroke(linewidth=3, foreground="#0a0a14")]
    ax.plot(*driver_loc, marker="s", color="#10b981", markersize=16, zorder=6,
            markeredgecolor="#fff", markeredgewidth=1.5)
    ax.annotate("DRIVER", driver_loc, textcoords="offset points", xytext=(12, 12),
                fontsize=8, color="#10b981", fontweight="bold", path_effects=mpe)
    ax.plot(*pickup, marker="^", color="#ec4899", markersize=16, zorder=6,
            markeredgecolor="#fff", markeredgewidth=1.5)
    ax.annotate("PICKUP", pickup, textcoords="offset points", xytext=(12, 12),
                fontsize=8, color="#ec4899", fontweight="bold", path_effects=mpe)
    ax.plot(*destination, marker="*", color="#a855f7", markersize=22, zorder=6,
            markeredgecolor="#fff", markeredgewidth=1.2)
    ax.annotate("DEST", destination, textcoords="offset points", xytext=(12, 12),
                fontsize=8, color="#a855f7", fontweight="bold", path_effects=mpe)

    legend_handles = [
        mpatches.Patch(color="#10b981", label="Driver"),
        mpatches.Patch(color="#ec4899", label="Pickup"),
        mpatches.Patch(color="#a855f7", label="Destination"),
    ]
    ax.legend(handles=legend_handles, loc="upper left", fontsize=7.5,
              facecolor="#150f24", edgecolor="#2d1b4e", labelcolor="#c9d1d9", framealpha=0.92)
    ax.set_xlim(-1, grid_size)
    ax.set_ylim(-1, grid_size)
    ax.set_xlabel("X", color="#484f58", fontsize=9, labelpad=8)
    ax.set_ylabel("Y", color="#484f58", fontsize=9, labelpad=8)
    ax.set_title("SafeHer - Secure Route Map", color="#c084fc", fontsize=12, fontweight="bold", pad=14)
    ax.tick_params(colors="#484f58", labelsize=7)
    for spine in ax.spines.values():
        spine.set_color("#2d1b4e")
    ax.set_aspect("equal")
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Fleet Map
# ---------------------------------------------------------------------------

def draw_fleet_map(drivers, pickup=None, destination=None, matched_id=None, grid_size=20):
    """Bird's-eye view of all drivers on the grid."""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    fig.patch.set_facecolor("#0a0a14")
    ax.set_facecolor("#0a0a14")

    for i in range(grid_size):
        ax.axhline(y=i, color="#1a1525", linewidth=0.2, zorder=1)
        ax.axvline(x=i, color="#1a1525", linewidth=0.2, zorder=1)

    for _, d in drivers.iterrows():
        c = "#10b981" if d["status"] == "available" else "#ef4444"
        alpha = 0.9 if d["status"] == "available" else 0.4
        sz = 8
        if d["driver_id"] == matched_id:
            c = "#f59e0b"
            sz = 14
            alpha = 1.0
            ax.annotate(d["driver_id"], (d["x"], d["y"]), textcoords="offset points",
                        xytext=(8, 8), fontsize=7, color="#f59e0b", fontweight="bold")
        ax.plot(d["x"], d["y"], "o", color=c, markersize=sz, alpha=alpha, zorder=3,
                markeredgecolor="#fff" if d["driver_id"] == matched_id else "none",
                markeredgewidth=1 if d["driver_id"] == matched_id else 0)

    if pickup:
        ax.plot(*pickup, marker="^", color="#ec4899", markersize=14, zorder=5,
                markeredgecolor="#fff", markeredgewidth=1.2)
    if destination:
        ax.plot(*destination, marker="*", color="#a855f7", markersize=16, zorder=5,
                markeredgecolor="#fff", markeredgewidth=1.2)

    legend_handles = [
        mpatches.Patch(color="#10b981", label="Available"),
        mpatches.Patch(color="#ef4444", label="Busy"),
        mpatches.Patch(color="#f59e0b", label="Matched"),
    ]
    ax.legend(handles=legend_handles, loc="upper left", fontsize=7,
              facecolor="#150f24", edgecolor="#2d1b4e", labelcolor="#c9d1d9", framealpha=0.9)
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_title("Fleet Overview - All Drivers", color="#c084fc", fontsize=11, fontweight="bold", pad=10)
    ax.tick_params(colors="#484f58", labelsize=6)
    for spine in ax.spines.values():
        spine.set_color("#2d1b4e")
    ax.set_aspect("equal")
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Path Timeline HTML
# ---------------------------------------------------------------------------

def build_path_timeline_html(pickup_path, trip_path, driver_loc, pickup, destination):
    """Return an HTML string rendering the route as a horizontal node timeline."""
    nodes = []
    nodes.append(
        f'<div class="path-node"><div class="path-dot pd-driver"></div>'
        f'<div class="path-coord">D {driver_loc[0]},{driver_loc[1]}</div></div>'
    )

    if pickup_path and len(pickup_path) > 2:
        step = max(len(pickup_path) // 3, 1)
        for i in range(step, len(pickup_path) - 1, step):
            p = pickup_path[i]
            nodes.append('<div class="path-connector pc-pickup"></div>')
            nodes.append(
                f'<div class="path-node"><div class="path-dot pd-mid"></div>'
                f'<div class="path-coord">{p[0]},{p[1]}</div></div>'
            )

    nodes.append('<div class="path-connector pc-pickup"></div>')
    nodes.append(
        f'<div class="path-node"><div class="path-dot pd-pickup"></div>'
        f'<div class="path-coord">P {pickup[0]},{pickup[1]}</div></div>'
    )

    if trip_path and len(trip_path) > 2:
        step = max(len(trip_path) // 3, 1)
        for i in range(step, len(trip_path) - 1, step):
            p = trip_path[i]
            nodes.append('<div class="path-connector pc-trip"></div>')
            nodes.append(
                f'<div class="path-node"><div class="path-dot pd-mid"></div>'
                f'<div class="path-coord">{p[0]},{p[1]}</div></div>'
            )

    nodes.append('<div class="path-connector pc-trip"></div>')
    nodes.append(
        f'<div class="path-node"><div class="path-dot pd-dest"></div>'
        f'<div class="path-coord">* {destination[0]},{destination[1]}</div></div>'
    )

    return '<div class="path-timeline">' + "".join(nodes) + "</div>"
