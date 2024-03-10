const AboutUs = () => (
      <section>
        <div className="max-w-6xl mx-auto px-4 sm:px-6">  
            {/* Section header */}
            <div className="max-w-3xl mx-auto text-center pb-12 md:pb-20">
              <p className="text-4xl font-bold text-gray-950">Meet The Team!</p>
              <h2 className="h2 mb-4"></h2>
              <p className="text-2xl text-gray-600">Learn more about the talented individuals who make up our team</p>
            </div>
  
            {/* Team Members */}
            <div className="max-w-sm mx-auto grid gap-8 lg:grid-cols-4 lg:gap-6 items-start lg:max-w-none">
  
              {/* 1st team member */}
              <div className="flex flex-col h-full p-6 bg-[#E9F7F5]" data-aos="fade-up">
                <div>
                  <div className="relative inline-flex flex-col mb-4">
                    <img className="rounded-full" src="profilePics/david_96.png" width={80} height={80} alt="Team Member 01" />
                  </div>
                </div>
                <blockquote className="text-xl text-gray-900 grow">   — GrizzHacks is an amazing experience! I learned a ton about new frameworks and technologies along with my amazing team. We are the best no doubt!
                 </blockquote>
                <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">
                  <cite className="text-[#84CCBF] not-italic">David G.</cite> - <span className="text-[#F0CD6C]">Objecct Detection Dev</span>
                </div>
              </div>
  
              {/* 2nd team member */}
              <div className="flex flex-col h-full p-6 bg-[#E9F7F5]" data-aos="fade-up" data-aos-delay="200">
                <div>
                  <div className="relative inline-flex flex-col mb-4">
                    <img className="rounded-full" src="profilePics/jaydin_96.png" width={80} height={80} alt="Team Member 02" />
                  </div>
                </div>
                <blockquote className="text-xl text-gray-900 grow">   — Spartahacks was undoubtedly my most successful hackathon to date. A huge shoutout to my incredible team; I couldn't have came close without them.
                </blockquote>
                <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">
                  <cite className="text-[#84CCBF] not-italic">Jaydin F.</cite> - <span className="text-[#F0CD6C]"> Object Detection Dev</span>
                </div>
              </div>
  
              {/* 3rd team member */}
              <div className="flex flex-col h-full p-6 bg-[#E9F7F5]" data-aos="fade-up" data-aos-delay="400">
                <div>
                  <div className="relative inline-flex flex-col mb-4">
                    <img className="rounded-full" src="profilePics/aaron_96.png" width={80} height={80} alt="Team Member 03" />
                  </div>
                </div>
                <blockquote className="text-xl text-gray-900 grow">   — GrizzHacks was my first hackathon. I had a lot of fun learning about Next.js and working with the team! 
                </blockquote>
                <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">
                  <cite className="text-[#84CCBF] not-italic">Aaron S.</cite> - <span className="text-[#F0CD6C]">Frontend Dev</span>
                </div>
              </div>
  
              {/* 4th team member */}
              <div className="flex flex-col h-full p-6 bg-[#E9F7F5]" data-aos="fade-up" data-aos-delay="400">
                <div>
                  <div className="relative inline-flex flex-col mb-4">
                    <img className="rounded-full" src="profilePics/luke_96.png" width={80} height={80} alt="Team Member 04" />
                  </div>
                </div>
                <blockquote className="text-xl text-gray-900 grow">   — I'm a Mechanical Engineer, and this is my first Hackathon, but I had a blast!
                 </blockquote>
                <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">
                  <cite className="text-[#84CCBF] not-italic">Luke F.</cite> - <span className="text-[#F0CD6C]">Hardware Dev</span>
                </div>
              </div>
  
            </div>
  
        </div>
      </section>
    );
    export { AboutUs };