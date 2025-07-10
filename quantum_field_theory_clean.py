from manim import *
import numpy as np

# Configuration for better rendering
config.media_width = "100%"
config.quality = "high_quality"

class QuantumFieldTheoryAnimation(ThreeDScene):
    def construct(self):
        # Scene 1: Introduction and Title
        self.scene_1_intro_title()

        # Scene 2: Quantum Field Concept
        self.scene_2_quantum_field()

        # Scene 3: Maxwell's Equations Transition
        self.scene_3_maxwell_equations()

        # Scene 4: QED Lagrangian Density
        self.scene_4_qed_lagrangian()

        # Scene 5: Feynman Diagram
        self.scene_5_feynman_diagram()

        # Scene 6: Running of the Coupling Constant
        self.scene_6_coupling_constant()

        # Scene 7: Final Collage and Summary
        self.scene_7_final_collage()

    def scene_1_intro_title(self):
        # Star field backdrop (simplified as dots)
        stars = VGroup(*[Dot(radius=0.05, color=WHITE).move_to(np.random.uniform(-7, 7, size=3))
                         for _ in range(200)])
        stars.set_opacity(0)
        self.add(stars)
        self.play(stars.animate.set_opacity(1), run_time=3)

        # Camera pan effect (simulated by shifting stars)
        self.play(stars.animate.shift(LEFT * 2), run_time=2)

        # Title fade-in
        title = Text("Quantum Field Theory: A Journey into the Electromagnetic Interaction",
                     font="CMU Serif", weight=BOLD, font_size=40)
        title.set_color_by_gradient(BLUE, PURPLE)
        title.set_opacity(0)
        self.play(title.animate.set_opacity(1).move_to(ORIGIN), run_time=2)
        self.wait(1)
        self.play(title.animate.scale(0.5).move_to(UP * 2.5 + LEFT * 3), run_time=1.5)

        # 3D Minkowski spacetime wireframe (simplified as axes and light cone)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(x_range=(-2, 2), y_range=(-2, 2), z_range=(-2, 2),
                          x_length=4, y_length=4, z_length=4)
        axes.get_z_axis().set_color(GRAY)
        axes.get_x_axis().set_color(YELLOW)
        axes.get_y_axis().set_color(YELLOW)
        self.add(axes)

        # Light cone (simplified as a cone)
        light_cone = Cone(base_radius=2, height=2, direction=UP, color=BLUE)
        light_cone.set_opacity(0.3)
        light_cone.move_to(ORIGIN)
        self.add(light_cone)

        # Metric equation
        metric_eq = MathTex(r"ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2", font_size=36)
        metric_eq.set_color_by_tex("-c^2 dt^2", RED)
        metric_eq.set_color_by_tex("dx^2", BLUE)
        metric_eq.set_color_by_tex("dy^2", GREEN)
        metric_eq.set_color_by_tex("dz^2", YELLOW)
        metric_eq.move_to(UP * 1.5 + RIGHT * 2)
        self.play(Write(metric_eq), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)

    def scene_2_quantum_field(self):
        # Zoom into origin (simulated by scaling down axes)
        self.move_camera(zoom=0.5, run_time=2)
        self.wait(1)

        # Electric and Magnetic field waves (simplified as sine waves)
        e_field = ParametricFunction(lambda t: np.array([t, np.sin(t * 2), 0]),
                                    t_range=(-PI, PI), color=RED)
        b_field = ParametricFunction(lambda t: np.array([t, 0, np.sin(t * 2)]),
                                    t_range=(-PI, PI), color=BLUE)
        e_field.move_to(ORIGIN)
        b_field.move_to(ORIGIN)
        self.play(Create(e_field), Create(b_field), run_time=2)

        # Labels and arrows
        e_label = MathTex(r"\vec{E}", color=RED).next_to(e_field, UP)
        b_label = MathTex(r"\vec{B}", color=BLUE).next_to(b_field, RIGHT)
        prop_arrow = Arrow(start=ORIGIN, end=RIGHT * 2, color=WHITE)
        self.play(Write(e_label), Write(b_label), GrowArrow(prop_arrow), run_time=1.5)
        self.wait(2)

    def scene_3_maxwell_equations(self):
        # Clear previous elements
        self.clear()
        self.set_camera_orientation(phi=0, theta=0)

        # Maxwell's equations (classical to relativistic)
        maxwell_classical = MathTex(r"\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}", font_size=36)
        maxwell_rel = MathTex(r"\partial_\mu F^{\mu \nu} = \mu_0 J^\nu", font_size=36)
        maxwell_classical.move_to(ORIGIN)
        self.play(Write(maxwell_classical), run_time=2)
        self.play(Transform(maxwell_classical, maxwell_rel), run_time=3)
        self.wait(1)
        self.play(maxwell_rel.animate.set_opacity(0.5).scale(1.2), run_time=1)
        self.wait(1)

    def scene_4_qed_lagrangian(self):
        # Semi-transparent plane
        plane = Rectangle(width=6, height=4, color=BLUE, fill_opacity=0.2)
        self.play(Create(plane), run_time=1)

        # QED Lagrangian
        lagrangian = MathTex(r"\mathcal{L}_{\text{QED}} = \bar{\psi}(i \gamma^\mu D_\mu - m)\psi - \frac{1}{4}F_{\mu\nu}F^{\mu\nu}",
                             font_size=36)
        lagrangian.set_color_by_tex(r"\psi", ORANGE)
        lagrangian.set_color_by_tex(r"D_\mu", GREEN)
        lagrangian.set_color_by_tex(r"\gamma^\mu", TEAL)
        lagrangian.set_color_by_tex(r"F_{\mu\nu}", GOLD)
        lagrangian.move_to(plane.get_center())
        self.play(Write(lagrangian), run_time=3)

        # Gauge transformation
        gauge_text = MathTex(r"e^{i \alpha(x)}", color=PURPLE).next_to(lagrangian, RIGHT)
        callout1 = Text("Gauge Transformation", font_size=24).next_to(gauge_text, UP)
        callout2 = Text("Charge Conservation", font_size=24).next_to(gauge_text, DOWN)
        self.play(Write(gauge_text), FadeIn(callout1), FadeIn(callout2), run_time=2)
        self.wait(2)

    def scene_5_feynman_diagram(self):
        self.clear()
        # Feynman diagram (simplified)
        electron1 = Line(start=LEFT * 3, end=ORIGIN, color=BLUE)
        electron2 = Line(start=RIGHT * 3, end=ORIGIN, color=BLUE)
        photon = DashedLine(start=ORIGIN, end=UP * 2, color=YELLOW)
        e1_label = MathTex(r"e^-", color=BLUE).next_to(electron1, LEFT)
        e2_label = MathTex(r"e^-", color=BLUE).next_to(electron2, RIGHT)
        gamma_label = MathTex(r"\gamma", color=YELLOW).next_to(photon, UP)
        self.play(Create(electron1), Create(electron2), Create(photon),
                  Write(e1_label), Write(e2_label), Write(gamma_label), run_time=2)

        # Interaction text
        interaction_text = Text("Electrons exchange a photon, the carrier of electromagnetic force.",
                                font_size=24).move_to(DOWN * 2)
        alpha_text = MathTex(r"\alpha \approx \frac{1}{137}", font_size=36).move_to(UP * 2.5)
        alpha_full = MathTex(r"\alpha = \frac{e^2}{4 \pi \epsilon_0 \hbar c}", font_size=36).move_to(UP * 2.5)
        self.play(FadeIn(interaction_text), Write(alpha_text), run_time=2)
        self.play(Transform(alpha_text, alpha_full), run_time=2)
        self.wait(2)

    def scene_6_coupling_constant(self):
        self.clear()
        # 2D graph for coupling constant
        axes = Axes(x_range=(0, 5), y_range=(0, 1), x_length=6, y_length=4,
                    axis_config={"include_numbers": True})
        x_label = Text("Energy Scale", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text("Coupling Strength", font_size=24).next_to(axes.y_axis, LEFT)
        curve = axes.plot(lambda x: 0.1 + 0.05 * x, x_range=(0, 5), color=BLUE)
        self.play(Create(axes), Write(x_label), Write(y_label), Create(curve), run_time=3)

        # Markers and captions
        energies = [1, 3]
        markers = VGroup(*[Dot(point=axes.c2p(i, 0.1 + 0.05 * i), color=RED) for i in energies])
        labels = VGroup(*[Text(f"{energy} GeV", font_size=18).next_to(marker, UP) for marker, energy in zip(markers, energies)])
        caption = Text("Virtual particle pairs shield charge, increasing α at higher energies.",
                       font_size=20).move_to(DOWN * 2.5)
        self.play(FadeIn(markers), FadeIn(labels), FadeIn(caption), run_time=2)
        self.wait(2)

    def scene_7_final_collage(self):
        self.clear()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Recreate simplified elements for collage
        axes = ThreeDAxes(x_range=(-1, 1), y_range=(-1, 1), z_range=(-1, 1))
        lagrangian = MathTex(r"\mathcal{L}_{\text{QED}}", font_size=24).move_to(UP * 1.5)
        feynman = Line(LEFT, RIGHT, color=BLUE).move_to(DOWN * 1.5)
        summary = Text("QED: Unifying Light and Matter Through Gauge Theory", font_size=30).move_to(ORIGIN)
        self.play(FadeIn(axes), FadeIn(lagrangian), FadeIn(feynman), FadeIn(summary), run_time=3)

        # Zoom out and return to star field
        self.move_camera(zoom=2, run_time=3)
        self.play(FadeOut(axes, lagrangian, feynman, summary), run_time=3)

        # Final subtitle
        finis = Text("Finis", font_size=24).move_to(DOWN * 2)
        self.play(FadeIn(finis), run_time=1)
        self.wait(1)
        self.play(FadeOut(finis, stars), run_time=2) 