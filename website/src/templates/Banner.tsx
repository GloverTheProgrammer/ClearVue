import Link from 'next/link';

import { Button } from '../button/Button';
import { CTABanner } from '../cta/CTABanner';
import { Section } from '../layout/Section';

const Banner = () => (
  <Section>
    <CTABanner
      title="Checkout our project!"
      subtitle="Visit our GitHub"
      button={
        <Link href="https://github.com/GloverTheProgrammer/ClearVue/">
          <Button>Get Started</Button>
        </Link>
      }
    />
  </Section>
);

export { Banner };
