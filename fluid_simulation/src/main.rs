mod particle;
mod app;

use eframe::egui;

fn main() -> eframe::Result<()> {
    let native_options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
        .with_inner_size([800.0, 600.0])
        .with_title("Fluid Simulation"),
        ..Default::default()
    };
    
    eframe::run_native(
        "Fluid Simulation",
        native_options,
        Box::new(|cc| Box::new(app::FluidApp::new(cc))),
    )
}
