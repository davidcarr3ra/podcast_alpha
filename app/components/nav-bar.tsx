import * as React from 'react';
import Link from 'next/link';

import {
  NavigationMenu,
  // NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  // NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu';

import { cn } from '@/lib/utils';

export default function NavBar() {
  return (
    <NavigationMenu className="z-[5] justify-between">
      <NavigationMenuList className="w-full">
				<NavigationMenuItem>
					<Link href="https://ui.shadcn.com/docs" legacyBehavior passHref>
						<NavigationMenuLink className={navigationMenuTriggerStyle()}>
							<span className="m750:max-w-[80px] m750:text-xs">
								DegenRadar
							</span>
						</NavigationMenuLink>
					</Link>
				</NavigationMenuItem>
      </NavigationMenuList>
			<NavigationMenuList className="w-full">
				<NavigationMenuItem>
						<Link href="/summary" legacyBehavior passHref>
							<NavigationMenuLink className={navigationMenuTriggerStyle()}>
								<span className="m750:max-w-[80px] m750:text-xs">
									Daily Summary
								</span>
							</NavigationMenuLink>
						</Link>
					</NavigationMenuItem>
					<NavigationMenuItem>
						<Link href="/chat" legacyBehavior passHref>
							<NavigationMenuLink className={navigationMenuTriggerStyle()}>
								<span className="m750:max-w-[80px] m750:text-xs">
									Chat
								</span>
							</NavigationMenuLink>
						</Link>
					</NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  );
}

const ListItem = React.forwardRef<
  React.ElementRef<'a'>,
  React.ComponentPropsWithoutRef<'a'>
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          ref={ref}
          className={cn(
            'hover:bg-accent block text-text select-none space-y-1 rounded-base border-2 border-transparent p-3 leading-none no-underline outline-none transition-colors hover:border-border dark:hover:border-darkBorder',
            className
          )}
          {...props}
        >
          <div className="text-base font-heading leading-none">{title}</div>
          <p className="text-muted-foreground font-base line-clamp-2 text-sm leading-snug">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  );
});
ListItem.displayName = 'ListItem';