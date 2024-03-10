const AboutUs = () => (
  <section>
    <div className="mx-auto max-w-6xl px-4 sm:px-6">
      <div className="mx-auto max-w-3xl pb-12 text-center md:pb-20">
        <p className="text-4xl font-bold text-gray-950">Meet The Team!</p>
        <h2 className="h2 mb-4"></h2>
        <p className="text-2xl text-gray-600">
          Learn more about the talented individuals who make up our team
        </p>
      </div>
      <div className="mx-auto grid max-w-sm items-start gap-8 lg:max-w-none lg:grid-cols-4 lg:gap-6">
        <div
          className="flex h-full flex-col bg-[#E9F7F5] p-6"
          data-aos="fade-up">
          <div>
            <div className="relative mb-4 inline-flex flex-col">
              <img className="rounded-full" src="profilePics/david_96.png" width={80} height={80} alt="Team Member 01" />
              </div>
          </div>
          <blockquote className="grow text-xl text-gray-900">   — GrizzHacks was amazing! I loved learning with the guys at Oakland University. We worked hard and very efficiently to make an excellent product. Go Bulldogs!
          </blockquote>
          <div className="mt-6 border-t border-gray-700 pt-5 font-medium text-gray-700">
            <cite className="not-italic text-[#84CCBF]">David G.</cite> - <span className="text-[#F0CD6C]">Object Detection Dev</span>
          </div>
        </div>
  
          {/* 2nd team member */}
          <div className="flex h-full flex-col bg-[#E9F7F5] p-6" data-aos="fade-up" data-aos-delay="200">
            <div>
              <div className="relative mb-4 inline-flex flex-col">
                <img className="rounded-full" src="profilePics/jaydin_96.png" width={80} height={80} alt="Team Member 02" />
              </div>
            </div>
            <blockquote className="grow text-xl text-gray-900">   — Spartahacks was undoubtedly my most successful hackathon to date. A huge shoutout to my incredible team; I couldn&apos;t have came close without them.
            </blockquote>
            <div className="mt-6 border-t border-gray-700 pt-5 font-medium text-gray-700">
              <cite className="not-italic text-[#84CCBF]">Jaydin F.</cite> - <span className="text-[#F0CD6C]"> Object Detection Dev</span>
            </div>
          </div>
  
          {/* 3rd team member */}
          <div className="flex h-full flex-col bg-[#E9F7F5] p-6" data-aos="fade-up" data-aos-delay="400">
            <div>
              <div className="relative mb-4 inline-flex flex-col">
                <img className="rounded-full" src="profilePics/aaron_96.png" width={80} height={80} alt="Team Member 03" />
              </div>
            </div>
            <blockquote className="grow text-xl text-gray-900">   — GrizzHacks was my first hackathon. I had a lot of fun learning about Next.js and working with the team! 
            </blockquote>
            <div className="mt-6 border-t border-gray-700 pt-5 font-medium text-gray-700">
              <cite className="not-italic text-[#84CCBF]">Aaron S.</cite> - <span className="text-[#F0CD6C]">Frontend Dev</span>
            </div>
          </div>
  
          {/* 4th team member */}
          <div className="flex h-full flex-col bg-[#E9F7F5] p-6" data-aos="fade-up" data-aos-delay="400">
            <div>
              <div className="relative mb-4 inline-flex flex-col">
                <img className="rounded-full" src="profilePics/luke_96.png" width={80} height={80} alt="Team Member 04" />
              </div>
            </div>
            <blockquote className="grow text-xl text-gray-900">   — I&apos;m a Mechanical Engineer, and this is my first Hackathon, but I had a blast!
            </blockquote>
            <div className="mt-6 border-t border-gray-700 pt-5 font-medium text-gray-700">
              <cite className="not-italic text-[#84CCBF]">Luke F.</cite> - <span className="text-[#F0CD6C]">Hardware Dev</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
  
  export { AboutUs };  