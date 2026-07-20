import { type ReactNode } from "react";

interface PageContainerProps {
  children: ReactNode;
}

const PageContainer = ({ children }: PageContainerProps) => {
  return (
    <main
      className="
        flex-1
        overflow-y-auto
        min-h-screen

        px-4
        py-6

        sm:px-6
        md:px-8
        lg:px-10
        xl:px-12
      "
    >
      {children}
    </main>
  );
};

export default PageContainer;