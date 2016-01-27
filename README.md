# About the project

Check it out: [https://ybogdanov.github.io/history-timeline/](https://ybogdanov.github.io/history-timeline/)

History Timeline is a visualization of the globally famous people lifetimes. It is inspired by Wait But Why's [blog post about Horizontal History](http://waitbutwhy.com/2016/01/horizontal-history.html) — the idea of taking a "horizontal" slice and see history's famous people alive at that time. However, I guess Tim Urban (the Wait But Why's author) had _too much_ fun manually drawing all of these rectangles in the [Numbers](http://www.apple.com/mac/numbers/) spreadsheet. The motivation of this project is to make the idea expandable, interactive, and crowd-sourced, by leveraging from the modern software engineering tools and approaches.

What you see is an open-source MVP that illustrates what's possible with relatively small software engineering effort. It is fun to use as is, but there is a ton of ideas of how the project can be improved further. I hope to engage other people in contributing and helping to evolve the visualization and data mining aspects of the tool.

What you can help with:

1. **Visualizations.** Having the data already provided to the browser, we can improve the way it is displayed.
2. **Data mining**. There is a common data mining pipeline setup, adding new sources was taken into account. The quality of the existing sources scraping can be also improved.
3. **Content**. Besides the programmatic part of data gathering, there's a possibility to tweak the data manually, make corrections, add new historical figures, etc.

There are a lot of glitches right now, such as zero aged people and some obviously popular figures missing on the timeline. The whole point is that you can fix all of it yourself!

If you have any questions/ideas/suggestions, or you have a contribution, feel free to [open an issue](https://github.com/ybogdanov/history-timeline/issues) or [a pull request](https://github.com/ybogdanov/history-timeline/pulls).

# Ideas of improvement

* Plot the most impactful historical events [from here](https://en.wikipedia.org/wiki/Timelines_of_world_history), so you can refer the events to the people lived that time
* Possibly, we can also display some personal events right on the people's rectangles
* Select the particular person so her lifespan is zoomed 90% horizontally, such way we can better inspect the life and the intersection with the other people
* Interactive overlay dialog that shows quick info of the person
* Hovering on a ruler can display a vertical cursor going down that highlights the people alive at that particular time
* We can show interactively how people relate each other in terms of different generations

Other ideas I've heard from people and not really into, but curious to see the implementations:

* Have an interactive map that can show people who are visible in the viewport
* iPad etc. native implementation
* Displaying avatars over the timeline rectangles

Things that have to be improved:

* Country filter is awful. There are too many countries and coloring them or filtering by the desired country is very inconvenient at the moment. Any ideas?
* The ruler is jumping when you scroll vertically. It's because it is scrolled with Javascript, not with CSS. If you have an idea how to make an element scrollable with the content horizontally, but stay sticky vertically with pure CSS, please suggest.

TODO: finish ideas

# How it works

TODO: Pantheon, Wikipedia, data pipeline, D3

# Contribute to visualizations
TODO

# Contribute to the content
TODO

# Contribute to data mining
TODO

TODO: layouts bugs and screenshots

```
# Make links from source data corpus to the local directory
ln -sf YOUR_STORAGE/people.json `pwd`/data/sources/pantheon.json
ln -sf YOUR_STORAGE/enwiki-20151201-pages-articles.xml `pwd`/data/sources/wikipedia.xml
```

Read Makefile to see how to get data files.

# Licensed under GPLv2

```
History Timeline is a visualization of the globally famous people lifetimes.
Copyright (C) 2016  Yuriy Bogdanov

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
```
