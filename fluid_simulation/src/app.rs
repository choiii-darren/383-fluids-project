use eframe::egui;
use egui::Color32;
use crate::particle::ParticleSystem;

pub struct FluidApp {
    particle_system: ParticleSystem,
    paused: bool,
    tube_length: f32,
    t_junction: bool,
    container_width: f32,
    container_height: f32,
}

impl FluidApp {
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {
        Self {
            particle_system: ParticleSystem::new(200.0, 300.0, 100.0, false),
            paused: false,
            tube_length: 100.0,
            t_junction: false,
            container_width: 200.0,
            container_height: 300.0,
        }
    }

    fn reset_simulation(&mut self) {
        self.particle_system = ParticleSystem::new(
            self.container_width,
            self.container_height,
            self.tube_length,
            self.t_junction,
        );
    }
}

impl eframe::App for FluidApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::SidePanel::left("controls").show(ctx, |ui| {
            ui.heading("Simulation Controls");
            
            if ui.button(if self.paused { "Resume" } else { "Pause" }).clicked() {
                self.paused = !self.paused;
            }
            
            if ui.button("Reset").clicked() {
                self.reset_simulation();
            }
            
            ui.add_space(20.0);
            ui.heading("Parameters");
            
            ui.horizontal(|ui| {
                ui.label("Tube Length:");
                if ui.add(egui::Slider::new(&mut self.tube_length, 50.0..=200.0)).changed() {
                    self.reset_simulation();
                }
            });
            
            ui.horizontal(|ui| {
                ui.label("Container Width:");
                if ui.add(egui::Slider::new(&mut self.container_width, 100.0..=400.0)).changed() {
                    self.reset_simulation();
                }
            });
            
            ui.horizontal(|ui| {
                ui.label("Container Height:");
                if ui.add(egui::Slider::new(&mut self.container_height, 100.0..=400.0)).changed() {
                    self.reset_simulation();
                }
            });
            
            ui.checkbox(&mut self.t_junction, "T-Junction");
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            let (response, painter) = ui.allocate_painter(
                ui.available_size(),
                egui::Sense::hover(),
            );
            
            let rect = response.rect;
            
            // Draw container
            painter.rect_stroke(
                rect,
                0.0,
                egui::Stroke::new(2.0, Color32::WHITE),
            );
            
            // Draw particles
            for particle in self.particle_system.get_particles() {
                let pos = egui::pos2(
                    rect.min.x + particle.position.x,
                    rect.min.y + particle.position.y,
                );
                
                painter.circle_filled(
                    pos,
                    2.0,
                    Color32::from_rgb(100, 149, 237),
                );
            }
            
            // Update simulation
            if !self.paused {
                self.particle_system.update(0.016); // ~60 FPS
            }
        });
        
        // Request continuous repaint
        ctx.request_repaint();
    }
} 