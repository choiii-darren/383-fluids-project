use glam::Vec2;
use rand::Rng;

pub struct Particle {
    pub position: Vec2,
    pub velocity: Vec2,
    pub life: f32,
}

impl Particle {
    pub fn new(position: Vec2, velocity: Vec2) -> Self {
        Self {
            position,
            velocity,
            life: 1.0,
        }
    }

    pub fn update(&mut self, dt: f32, gravity: f32) {
        self.velocity.y += gravity * dt;
        self.position += self.velocity * dt;
        self.life -= dt * 0.5; // Particles slowly fade out
    }
}

pub struct ParticleSystem {
    particles: Vec<Particle>,
    container_bounds: (Vec2, Vec2), // (min, max) corners
    tube_start: Vec2,
    tube_end: Vec2,
    t_junction: bool,
    t_junction_end: Option<Vec2>,
}

impl ParticleSystem {
    pub fn new(
        container_width: f32,
        container_height: f32,
        tube_length: f32,
        t_junction: bool,
    ) -> Self {
        let container_bounds = (
            Vec2::new(50.0, 50.0),
            Vec2::new(50.0 + container_width, 50.0 + container_height),
        );
        
        let tube_start = Vec2::new(
            container_bounds.0.x + container_width * 0.5,
            container_bounds.1.y,
        );
        
        let tube_end = tube_start + Vec2::new(0.0, tube_length);
        
        let t_junction_end = if t_junction {
            Some(tube_end + Vec2::new(50.0, 0.0))
        } else {
            None
        };

        Self {
            particles: Vec::new(),
            container_bounds,
            tube_start,
            tube_end,
            t_junction,
            t_junction_end,
        }
    }

    pub fn update(&mut self, dt: f32) {
        let mut rng = rand::thread_rng();
        
        // Emit new particles at water surface
        if self.particles.len() < 1000 {
            let water_surface_y = self.container_bounds.1.y - 50.0; // Adjust based on current water level
            let x = rng.gen_range(self.container_bounds.0.x..self.container_bounds.1.x);
            let pos = Vec2::new(x, water_surface_y);
            let vel = Vec2::new(0.0, rng.gen_range(0.0..50.0));
            self.particles.push(Particle::new(pos, vel));
        }

        // Update existing particles
        for particle in &mut self.particles {
            particle.update(dt, 98.1); // 10x gravity for more visible effect
            
            // Basic collision with container walls
            if particle.position.x < self.container_bounds.0.x {
                particle.position.x = self.container_bounds.0.x;
                particle.velocity.x *= -0.5;
            }
            if particle.position.x > self.container_bounds.1.x {
                particle.position.x = self.container_bounds.1.x;
                particle.velocity.x *= -0.5;
            }
            
            // Flow through tube
            if particle.position.y > self.tube_start.y {
                let tube_radius = 10.0;
                if (particle.position.x - self.tube_start.x).abs() < tube_radius {
                    particle.velocity.y += 200.0 * dt; // Accelerate through tube
                }
            }
            
            // T-junction behavior
            if self.t_junction && particle.position.y > self.tube_end.y {
                if let Some(t_end) = self.t_junction_end {
                    particle.velocity.x += 100.0 * dt; // Flow towards T-junction end
                }
            }
        }

        // Remove dead particles
        self.particles.retain(|p| p.life > 0.0);
    }

    pub fn get_particles(&self) -> &[Particle] {
        &self.particles
    }
} 