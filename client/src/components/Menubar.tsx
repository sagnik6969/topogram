import { Search, Square, Circle, MousePointer2, Group } from "lucide-react";
import { useMemo } from "react";
// import React from 'react';

function MenubarItem({ icon: Icon }: any) {
  return (
    <button className="p-3 hover:bg-slate-100 m-1 rounded">
      {<Icon size={14} />}
    </button>
  );
}

function Menubar() {
  const menubarItems = useMemo(
    () => [
      {
        icon: Search,
      },
      {
        icon: Square,
      },
      {
        icon: Circle,
      },
      {
        icon: MousePointer2,
      },
      {
        icon: Group,
      },
    ],
    []
  );

  return (
    <div className="bg-background border-slate-200 border rounded-sm flex flex-col items-center justify-center w-fit shadow-md fixed top-[30%] left-3 z-50">
      {menubarItems.map((item, index) => (
        <MenubarItem key={index} icon={item.icon} />
      ))}
    </div>
  );
}

export default Menubar;
