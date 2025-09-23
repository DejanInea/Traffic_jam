"""PyQt6 traffic jam simulation."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


TRACK_LENGTH = 1200.0  # virtual length of the one-lane loop
JAM_START = 520.0  # position where the congestion begins
JAM_END = 700.0  # end of the congested zone
CAR_LENGTH = 42.0
CAR_WIDTH = 18.0
MAX_SPEED = 140.0  # px / s
MIN_SPEED = 18.0
SAFE_GAP = 28.0
ACCELERATION = 70.0
BRAKING = 110.0
FPS = 60


@dataclass
class Car:
    x: float
    speed: float
    color: QColor
    braking: float = 0.0


class SimulationWidget(QWidget):
    def __init__(self, car_count: int = 14, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(900, 340)
        self._rng = random.Random()
        self._dt = 1.0 / FPS
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.advance)
        self._timer.start(int(self._dt * 1000))
        self._paused = False
        self._cars: List[Car] = []
        self._generate_cars(car_count)

    def _generate_cars(self, count: int) -> None:
        self._cars.clear()
        base_gap = TRACK_LENGTH / count
        offset = self._rng.random() * base_gap
        for idx in range(count):
            x = (offset + idx * base_gap) % TRACK_LENGTH
            hue = int((idx * 37) % 360)
            color = QColor.fromHsv(hue, 150, 240)
            initial_speed = MAX_SPEED * 0.4 + self._rng.random() * 10
            self._cars.append(Car(x=x, speed=initial_speed, color=color))

    def toggle_pause(self) -> None:
        self._paused = not self._paused

    def reset(self) -> None:
        self._generate_cars(len(self._cars))

    @property
    def paused(self) -> bool:
        return self._paused

    @property
    def average_speed(self) -> float:
        if not self._cars:
            return 0.0
        return sum(car.speed for car in self._cars) / len(self._cars)

    def advance(self) -> None:
        if self._paused:
            self.update()
            return

        ordered = sorted(self._cars, key=lambda car: car.x)
        for index, car in enumerate(ordered):
            lead = ordered[(index + 1) % len(ordered)]
            lead_x = lead.x
            if lead_x <= car.x:
                lead_x += TRACK_LENGTH
            gap = lead_x - car.x - CAR_LENGTH

            desired = self._desired_speed(car.x, gap)
            self._apply_speed(car, desired, self._dt)
            car.x = (car.x + car.speed * self._dt) % TRACK_LENGTH

        self.update()

    def _desired_speed(self, position: float, gap: float) -> float:
        desired = MAX_SPEED

        slowdown_factor = self._slowdown_factor(position)
        desired = min(desired, MAX_SPEED * slowdown_factor)

        if gap < SAFE_GAP:
            desired = min(desired, MIN_SPEED * max(gap / SAFE_GAP, 0.2))
        elif gap < SAFE_GAP * 2.5:
            desired = min(desired, MAX_SPEED * (0.35 + 0.65 * (gap / (SAFE_GAP * 2.5))))

        return max(MIN_SPEED * 0.5, desired)

    def _slowdown_factor(self, position: float) -> float:
        if JAM_START <= position <= JAM_END:
            return MIN_SPEED / MAX_SPEED

        distance = self._distance_to_zone(position, JAM_START)
        if distance < 160.0:
            blend = distance / 160.0
            return 0.25 + 0.75 * blend
        return 1.0

    def _distance_to_zone(self, position: float, zone_start: float) -> float:
        if zone_start >= position:
            return zone_start - position
        return TRACK_LENGTH - position + zone_start

    def _apply_speed(self, car: Car, target: float, dt: float) -> None:
        if car.speed < target:
            car.speed = min(target, car.speed + ACCELERATION * dt)
            car.braking = max(0.0, car.braking - dt * 3)
        else:
            car.speed = max(target, car.speed - BRAKING * dt)
            car.braking = min(1.0, car.braking + dt * 3)

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        margin = 60
        road_height = 90
        road_top = (height - road_height) / 2
        scale = (width - margin * 2) / TRACK_LENGTH

        painter.fillRect(self.rect(), QColor(30, 32, 38))

        road_rect = QRectF(margin, road_top, width - margin * 2, road_height)
        painter.setBrush(QColor(54, 59, 66))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(road_rect, 16, 16)

        jam_rect = QRectF(
            margin + JAM_START * scale,
            road_top,
            max((JAM_END - JAM_START) * scale, 6.0),
            road_height,
        )
        painter.setBrush(QColor(176, 74, 74, 180))
        painter.drawRoundedRect(jam_rect, 14, 14)

        lane_pen = QPen(QColor(240, 240, 240, 150))
        lane_pen.setWidth(2)
        lane_pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(lane_pen)
        painter.drawLine(margin, road_top + road_height / 2, width - margin, road_top + road_height / 2)

        painter.setPen(Qt.PenStyle.NoPen)
        for car in self._cars:
            center_x = margin + car.x * scale
            car_width = CAR_LENGTH * scale
            car_height = CAR_WIDTH
            car_rect = QRectF(
                center_x - car_width / 2,
                road_top + road_height / 2 - car_height / 2,
                car_width,
                car_height,
            )
            painter.setBrush(car.color)
            painter.drawRoundedRect(car_rect, 6, 6)

            brake_width = car_width * 0.18
            brake_rect = QRectF(
                car_rect.left(),
                car_rect.top(),
                brake_width,
                car_rect.height(),
            )
            brake_intensity = int(120 + 135 * car.braking)
            painter.setBrush(QColor(220, 30, 30, brake_intensity))
            painter.drawRoundedRect(brake_rect, 4, 4)

        painter.setPen(QColor(230, 230, 230))
        painter.setFont(QFont("Segoe UI", 10))
        info_text = (
            f"Avti: {len(self._cars)}    "
            f"Povp. hitrost: {self.average_speed * 0.12:.1f} km/h    "
            f"Pavza: {'da' if self._paused else 'ne'}"
        )
        painter.drawText(
            margin,
            road_top - 20,
            info_text,
        )

        subtitle = "Rdece obarvano obmocje predstavlja zastoj, vozila pred njim upocasnjujejo."
        painter.drawText(margin, road_top + road_height + 30, subtitle)

    def sizeHint(self):  # type: ignore[override]
        return self.minimumSize()


class TrafficWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Simulacija zastoja na cesti")
        self._simulation = SimulationWidget()
        self._build_ui()
        self._status_timer = QTimer(self)
        self._status_timer.timeout.connect(self._refresh_status)
        self._status_timer.start(400)

    def _build_ui(self) -> None:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        layout.addWidget(self._simulation, stretch=1)

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self._pause_button = QPushButton("Pavza")
        self._pause_button.clicked.connect(self._handle_pause)
        controls.addWidget(self._pause_button)

        reset_button = QPushButton("Ponastavi")
        reset_button.clicked.connect(self._simulation.reset)
        controls.addWidget(reset_button)

        controls.addStretch(1)

        self._status_label = QLabel()
        self._status_label.setMinimumWidth(240)
        controls.addWidget(self._status_label)

        layout.addLayout(controls)
        self.setCentralWidget(container)

    def _handle_pause(self) -> None:
        self._simulation.toggle_pause()
        self._pause_button.setText("Nadaljuj" if self._simulation.paused else "Pavza")
        self._refresh_status()

    def _refresh_status(self) -> None:
        speed = self._simulation.average_speed * 0.12
        status = f"Povp. hitrost: {speed:.1f} km/h"
        if self._simulation.paused:
            status += " | Pavza"
        self._status_label.setText(status)


def main() -> None:
    app = QApplication([])
    window = TrafficWindow()
    window.resize(980, 480)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
