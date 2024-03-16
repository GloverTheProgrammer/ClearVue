import { VerticalFeatureRow } from '../feature/VerticalFeatureRow';
import { Section } from '../layout/Section';

const VerticalFeatures = () => (
  <Section
    title="Empowering Vision"
    description="Globally, an estimated 40 to 45 million people are blind and 135 million have low vision. Utilizing the GPT-4 AI model and advanced sensory technology, our mission is to help these individuals 
    regain the ability to live thier every-day lives!"
  >
  <center>
  <video src='videos/demo2.mp4' width="800" height="400" controls />
  </center>
    <VerticalFeatureRow
      title="In Front"
      description='Our "In Front" feature, is designed to revolutionize the way individuals with visual impairments interact with their surroundings. This feature provides a short real-time auditory feedback, enabling users to identify objects in their immediate environment.'
      image="assets/images/music-plate-svgrepo-com.svg"
      imageAlt="First feature alt text"
    />
    <VerticalFeatureRow
      title="Story Mode"
      description="Our Story Mode feature creates a narrative of the user's environment, providing a comprehensive understanding of their surroundings. It's like having a personal narrator for the world around them, enhancing their interaction and experience."
      image="assets/images/text-view-svgrepo-com.svg"
      imageAlt="Second feature alt text"
      reverse
    />
    <VerticalFeatureRow
      title="Reading Mode"
      description="Designed with user accessibility in mind, our Reading Mode feature is specifically developed to allow users to read labels that are positioned in their immediate vicinity. Instead of struggling with small fonts or complex words, users can now easily comprehend labels in their surroundings."
      image="assets/images/color-block-exclamation-svgrepo-com.svg"
      imageAlt="Third feature alt text"
    />
    
    <VerticalFeatureRow
      title="Active Detection Mode"
      description="Our Active Detection feature is designed with mobility in mind! Perfect for users who are constantly on the move, users are not only able to detect the presence of objects but also identify their count and type. This feature provides an auditory feedback of the immediate environment in real-time, adding a new dimension to their sensory experience."
      image="assets/images/searcher-svgrepo-com.svg"
      imageAlt="Fourth feature alt text"
      reverse
    />
  </Section>
);

export { VerticalFeatures };
