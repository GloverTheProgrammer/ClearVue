import { VerticalFeatureRow } from '../feature/VerticalFeatureRow';
import { Section } from '../layout/Section';

const VerticalFeatures = () => (
  <Section
    title="Empowering Vision"
    description="Globally, an estimated 40 to 45 million people are blind and 135 million have low vision. Utilizing the GPT-4 AI model and advanced sensory technology, our mission is to help these individuals 
    regain the ability to live thier every-day lives!"
  >
    <VerticalFeatureRow
      title="What's in front?"
      description='Our "What’s in Front?" feature, is designed to revolutionize the way individuals with visual impairments interact with their surroundings. This feature provides a short real-time auditory feedback, enabling users to identify objects in their immediate environment.'
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
      title="Reading Lables"
      description="Designed with user accessibility in mind, our Reading Labels feature is specifically developed to allow users to read labels that are positioned in their immediate vicinity. Instead of struggling with small fonts or complex words, users can now easily comprehend labels in their surroundings."
      image="assets/images/color-block-exclamation-svgrepo-com.svg"
      imageAlt="Third feature alt text"
    />
  </Section>
);

export { VerticalFeatures };
